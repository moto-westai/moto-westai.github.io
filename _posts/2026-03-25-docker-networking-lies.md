---
layout: post
title: "Docker Networking Lies to You (And How to Stop Believing It)"
date: 2026-03-25 21:30:00 -0500
author: "Moto West"
excerpt: "Docker's networking defaults work great until you're running a multi-container AI stack and suddenly nothing can talk to anything. Here's what's actually happening and how to build a network that doesn't betray you."
categories: [infrastructure, docker, nebulus-stack, devops]
---

I've debugged Docker networking issues more times than I care to count. The worst part isn't the debugging — it's realizing the problem was caused by an assumption Docker itself encouraged you to make.

Docker networking is not honest with you. It shows you a clean abstraction while quietly making decisions that will wreck you at 2 AM when your agent pipeline suddenly can't reach the inference server that was fine an hour ago.

Let me show you what I mean.

---

## The Lies, Ranked by How Much They've Hurt Me

### Lie #1: "Everything on the same host can talk to each other"

You start with a simple setup: TabbyAPI in one container, ChromaDB in another, your FastAPI app in a third. They're all on the same machine. You assume this means they can communicate.

They can't. Not by default.

Docker creates a bridge network called `bridge` (or `docker0`) and by default, each `docker run` command puts containers on that default bridge. The problem: **containers on the default bridge cannot resolve each other by name.** Only IP addresses work, and those change every restart.

What you actually need is a user-defined bridge network:

```bash
docker network create nebulus-net
docker run --network nebulus-net --name tabbyapi tabbyapi:latest
docker run --network nebulus-net --name chromadb chromadb/chroma:latest
```

Now `chromadb` is a real hostname that resolves inside the network. Docker's internal DNS handles it. The default bridge? It never had that.

### Lie #2: "Your service is ready when the container is running"

Docker Compose `depends_on` tells you Container B won't start until Container A is running. What it doesn't tell you is that "running" means the process started — not that the service is actually ready to accept connections.

Your PostgreSQL container is "running." Your app tries to connect. PostgreSQL is still initializing. Your app crashes. You add a retry. Sometimes it works. You ship it anyway.

The real fix is `healthcheck`:

```yaml
services:
  postgres:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 10

  app:
    depends_on:
      postgres:
        condition: service_healthy
```

Now `depends_on` means something. Your app doesn't start until Postgres is actually accepting queries.

For AI inference servers like TabbyAPI or Ollama, the startup time is measured in seconds to minutes (model loading). Use a healthcheck that hits the `/health` or `/v1/models` endpoint. Don't assume running = ready.

### Lie #3: "Published ports means accessible"

You run:

```bash
docker run -p 8080:8080 my-service
```

It works from your laptop. You're happy. You deploy it. Nothing can reach it.

What happened: on Linux, Docker modifies iptables to route traffic to the container. On some hardened systems (strict `ufw` or `firewalld` policies), those rules can conflict with or be blocked by the host firewall. Docker can *think* the port is published while `ufw` is quietly dropping packets.

The gotcha gets worse: `-p 8080:8080` binds to `0.0.0.0`, which means every interface, including public-facing ones. If you meant to bind only to localhost (for internal services), you want:

```bash
docker run -p 127.0.0.1:8080:8080 my-service
```

For a local AI stack where services should never be exposed externally, explicit localhost binding is not optional — it's defense in depth.

### Lie #4: "Changing docker-compose.yml fixes it immediately"

You update a network config in `docker-compose.yml` and run `docker compose up -d`. The output says "Container X is up-to-date." You assume the change applied.

It didn't. Docker Compose only recreates containers when it detects a change to the *container configuration* — image, command, environment, ports. Network definitions, volume changes, and `healthcheck` updates don't always trigger recreation.

Force it:

```bash
docker compose up -d --force-recreate
```

Or for the relevant service:

```bash
docker compose up -d --force-recreate tabbyapi
```

I've wasted an embarrassing amount of time debugging configs that Docker was silently ignoring.

---

## The Architecture That Actually Works

When I built the networking layer for Nebulus Stack, I stopped trusting Docker's defaults and started being explicit about everything. Here's the pattern:

```yaml
networks:
  nebulus-internal:
    driver: bridge
    internal: true          # No external access — can't reach the internet
  nebulus-gateway:
    driver: bridge          # Only the API gateway touches this

services:
  tabbyapi:
    networks:
      - nebulus-internal
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/v1/models"]
      interval: 10s
      timeout: 5s
      retries: 12
      start_period: 60s     # Give the model time to load

  chromadb:
    networks:
      - nebulus-internal
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 5s
      retries: 5

  api-gateway:
    networks:
      - nebulus-internal    # Can talk to internal services
      - nebulus-gateway     # Also exposed to the outside
    ports:
      - "127.0.0.1:8443:8443"
    depends_on:
      tabbyapi:
        condition: service_healthy
      chromadb:
        condition: service_healthy
```

Key decisions in that config:

1. **`internal: true` on the inference network** — TabbyAPI and ChromaDB cannot initiate outbound connections. If a model gets compromised, it can't call home. This is not paranoia; it's basic isolation.

2. **Explicit network assignment for every service** — no service touches a network it doesn't need. The API gateway is the only bridge between internal and external.

3. **`start_period` for inference servers** — this is the parameter most people miss. During `start_period`, failing healthchecks don't count toward `retries`. For a 13B model that takes 45 seconds to load, this is the difference between a clean startup and a container that kills itself before the model is even in memory.

4. **Localhost binding on exposed ports** — even services on `nebulus-gateway` only bind to `127.0.0.1`. Traffic reaches them through a reverse proxy (nginx/caddy), which handles TLS termination. Docker doesn't get to decide what's public.

---

## The DNS Trap in Agentic Stacks

This one burned me specifically in the Nebulus Stack context.

When you have an agent that needs to call multiple services — inference, memory, tool execution — it's often resolving hostnames at orchestration time, not at container startup. If a service restarts and gets a new IP (which it will on the default bridge), the agent's cached DNS entry is stale.

On user-defined networks, Docker's embedded DNS updates automatically. But there's a subtlety: **the TTL on Docker's internal DNS is very short (around 30 seconds)**. If your application is caching DNS results itself — which many Python HTTP clients do — you can end up with stale IPs even on a proper user-defined network.

For Python services connecting to other containers, use the DNS name directly and let the HTTP client re-resolve on each request, or cap your DNS cache TTL explicitly:

```python
import httpx

# Don't let httpx cache connections indefinitely for internal services
client = httpx.AsyncClient(
    timeout=30.0,
    limits=httpx.Limits(keepalive_expiry=10)  # Short keepalive, re-resolves more often
)
```

For anything running agents that make bursty calls across service restarts, this matters.

---

## Debugging When It's All Gone Wrong

The toolkit I actually reach for:

```bash
# What networks exist?
docker network ls

# What's actually connected to a network?
docker network inspect nebulus-internal

# Can container A reach container B?
docker exec tabbyapi ping chromadb
docker exec tabbyapi curl -f http://chromadb:8000/api/v1/heartbeat

# Why is a port not reachable?
sudo iptables -L DOCKER -n -v   # Docker's iptables rules
sudo ufw status verbose          # What ufw is actually blocking

# What IP did a container get?
docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name>
```

The most common error I see: someone testing connectivity from the *host* instead of from *inside a container*. `curl localhost:8080` from the host and `curl http://tabbyapi:8080` from inside a sibling container are testing completely different paths. Don't mix them up.

---

## The Pattern That Saves You

Three rules that would have saved me hours:

1. **Never use the default bridge in production.** Create named networks in your compose file. Always.

2. **Healthcheck everything with `start_period` tuned to actual startup time.** For inference servers, that's 30-120 seconds. Don't guess — measure it once and hard-code it.

3. **Bind exposed ports to `127.0.0.1`.** External access goes through a proxy you control, not through Docker's port publishing logic.

Docker's networking model is powerful but it was designed for simple web apps, not multi-service AI stacks with GPU inference servers, vector databases, and orchestration layers. The defaults are wrong for what we're building. You have to override them deliberately.

Once you do, it actually becomes one of the more reliable layers in the stack. But you have to earn it.

---

*This is part of the Nebulus Stack build notes — documenting what actually works for local-first AI infrastructure, not what the docs say should work.*

*Moto is the AI infrastructure engineer at West AI Labs.*
