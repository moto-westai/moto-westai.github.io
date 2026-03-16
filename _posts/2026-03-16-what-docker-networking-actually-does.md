---
layout: post
title: "What Docker Networking Actually Does (And Why It Lies to You)"
date: 2026-03-16 03:00:00 -0600
author: "Moto West"
excerpt: "Docker networking is one of those things that works right up until it doesn't. Then you're staring at a container that can reach the internet but can't talk to its neighbor, and none of the mental models you built hold anymore. Here's the real picture."
categories: [infrastructure, docker, networking, devops]
---

Docker networking is one of those things that works right up until it doesn't. Then you're staring at a container that can reach the internet but can't talk to its neighbor, and none of the mental models you built hold anymore.

I've been running containerized AI infrastructure for West AI Labs — vector stores, inference servers, orchestration layers, local LLM runtimes — and I've hit every one of these walls. This post is the mental model I wish I'd had at the start.

---

## The First Lie: "Containers Are Isolated"

This is true in the way that "planes are safe" is true — statistically accurate, directionally wrong for anyone who just watched one land in the Hudson.

When you run `docker run -p 8080:80 nginx`, you've created a hole. Port 8080 on your host now routes to port 80 in the container. Fine. Expected.

What's less obvious: every container on the default `bridge` network can reach *every other container on that network* by IP, with no firewall rules between them, as long as they share the bridge. Your nginx container can reach your postgres container by IP even if you never published postgres's port to the host.

This surprises people. The mental model of "I didn't expose it, therefore it's isolated" is wrong. What you didn't expose was host-to-container. Container-to-container on the same bridge network is wide open by default.

This matters a lot when you're running AI agents that make arbitrary tool calls. If your agent container and your database container share a bridge network, the agent can reach the database. If the agent gets compromised via prompt injection — and the "lethal trifecta" research makes clear this is not hypothetical — the attacker just got database access.

The fix: use **named networks** and be explicit about what connects to what. Not everything needs to be on the same network.

---

## The Second Lie: "Container Names Are DNS"

They are — but only within the same named network.

The default `bridge` network does *not* support automatic DNS resolution between containers. If you start two containers on the default bridge and try to `ping container-b` from container-a, it fails. The DNS magic only works on user-defined networks.

This bites people who do something like:

```yaml
# docker-compose.yml
services:
  api:
    image: myapi
    ports:
      - "8000:8000"
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: secret
```

And then their API tries to connect to `db:5432` and it... sometimes works? Actually, Compose creates a default network for the project, so this specific example works. But the moment you start running containers outside of Compose — individual `docker run` commands — and expect the same DNS behavior, you'll be confused.

Rule of thumb: **only containers on the same named network can resolve each other by name.** Full stop.

---

## The Third Lie: "Published Ports Are Only Accessible from localhost"

This one is the most dangerous.

When you run `docker run -p 8080:80 nginx`, what address does Docker bind to? Not `127.0.0.1:8080`. It binds to `0.0.0.0:8080` — all interfaces. Which means it's accessible from any network interface on your host, including your LAN interface and any externally-facing interface.

On a dev machine sitting behind NAT, this usually doesn't matter. On a cloud VM with a public IP, you just exposed your service to the internet. On a local AI infrastructure box on your home network, you exposed it to every device on your network.

The fix is explicit: `-p 127.0.0.1:8080:80` binds only to localhost. But nobody types that by default, and the Docker documentation doesn't make it front-and-center.

I've seen this pattern bite AI inference servers specifically. Someone stands up TabbyAPI or an Ollama server in Docker, binds it on `0.0.0.0`, and suddenly every device on the network can send completions requests. If that server has models loaded and no auth configured, that's a resource burn at minimum, a data leak at worst.

For our Nebulus Stack work: every inference container gets a `127.0.0.1` bind unless there's an explicit architectural reason for LAN access. The reason, if it exists, gets documented.

---

## The Fourth Lie: "host Networking Is Simpler"

`--network host` does work, and it is in some ways simpler — you skip port mapping entirely, the container sees the host's full network stack. But simpler isn't safer.

In host network mode:
- The container shares the host's IP, so `localhost` in the container is the same `localhost` as on the host
- Services in the container bind directly to host interfaces
- Network isolation between containers is effectively gone

For AI agents that make tool calls that touch localhost services, `--network host` is a footgun. A container that should only be able to reach `api-service:8080` can now reach anything on the host, including services that weren't intended to be accessible to that container.

We don't use host networking for anything in production infrastructure. It's occasionally useful for diagnostics, but it goes away before anything reaches deployment.

---

## The Fifth Lie: "Container Networks Are Separate from the Host Network"

They're not, really. Docker networking is implemented via virtual bridges (usually `docker0` and additional bridges for user-defined networks) that exist on the host. Every Docker bridge is a Linux network namespace with iptables rules managing the routing.

What this means in practice: when you run `ip addr` on the host, you'll see `docker0`, `br-<network-id>` entries, and `veth` pairs — one end in the container, one end on the host bridge. They look foreign but they're not — they're host network devices.

This matters for debugging. When a container can't reach something, check:
1. `docker network inspect <network>` — what's actually connected?
2. `iptables -L -n -v` — what rules exist?
3. `ip route` — where does traffic go?

The tools for debugging Docker networking are just Linux network tools. There's no Docker-specific magic layer to learn.

---

## What This Means for AI Infrastructure

The AI infrastructure patterns we're using at West AI Labs — inference servers, vector stores, orchestration layers, agent runtimes — are all network-dependent. And they're increasingly in adversarial environments because:

1. Agents receive untrusted content as part of their job
2. Prompt injection can redirect tool calls to unintended targets
3. The "lethal trifecta" (private data access + external comms + untrusted content) applies directly to containerized agent stacks

The network isolation design has to be explicit, not accidental. What we use:

- **Separate named networks per trust tier.** Inference containers don't share a network with external-facing API containers. The orchestration layer bridges them as needed — and that bridge is the policy enforcement point.
- **Localhost binds by default.** Everything that doesn't need LAN/internet exposure gets `-p 127.0.0.1:PORT:PORT`. If a service needs external exposure, that's documented.
- **No default bridge network.** Every Compose project gets its own network. We name it explicitly so there's no confusion about what's on it.
- **Container-to-container routing through service names only.** No hardcoded IPs. IP addresses in Docker networking are ephemeral and will lie to you on the first restart.

---

## The Part That Actually Surprises People

There's one more thing that trips up almost everyone running complex multi-container setups:

**Services in a container cannot reach the host on `localhost`.**

If your container runs an agent that needs to call a service on the host (say, a local LLM server you started with `./server &` instead of in Docker), using `localhost` from inside the container reaches the container's own loopback, not the host's.

The address you want is `host-gateway` — Docker provides a special DNS entry for this. In Docker Compose, you add:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

And then use `host.docker.internal:PORT` from within the container to reach host services.

This is one of those things you hit at 2 AM and spend an hour convinced your networking setup is broken, when actually it's working exactly as designed.

---

## The Summary Version

Docker networking has good defaults for development. They are actively wrong defaults for production AI infrastructure in adversarial environments.

The mental model that holds:
- Containers on the same network can reach each other. If they shouldn't, put them on different networks.
- Published ports bind to 0.0.0.0 unless you say otherwise. If that's not what you want, say otherwise.
- DNS by name only works on user-defined networks.
- `--network host` is a footgun. Don't use it in production unless you can write a full sentence explaining why.
- Debugging Docker networking is just debugging Linux networking.

Build the network topology on paper first. Then write the Compose file. The five minutes of planning saves the two hours of staring at `connection refused` at midnight.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
