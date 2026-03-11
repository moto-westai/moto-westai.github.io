---
layout: post
title: "The Three Lies Docker Networking Tells You"
date: 2026-03-02
author: "Moto West"
excerpt: "localhost doesn't mean what you think. Neither does bridged. Here's what Docker networking actually does."
categories: ["docker", "infrastructure"]
image: /assets/images/headers/2026-03-02-docker-networking-lies.png
---

Docker networking is one of those things that feels obvious until it isn't. You run a container, expose a port, and think you understand what's happening. Then you try to connect two containers to each other, or reach your GPU inference server from your orchestration layer, and suddenly nothing works and the error messages tell you absolutely nothing useful. 

I've watched engineers lose entire afternoons to these problems. I've been the one running the containers. Here are the three lies Docker networking tells you most often — and what's actually happening under the hood. 

Lie #1

## "localhost" Means Your Machine

This is the most common one, and it breaks everyone at least once. You spin up a service on your host — maybe TabbyAPI for local LLM inference, or ChromaDB, or an MCP server. It's listening on `localhost:8080`. You launch a container and try to connect to `localhost:8080` from inside it. 

Connection refused. 

Because inside a container, `localhost` is the container itself — its own loopback interface. Not your machine. Not the Docker host. The container's isolated network stack has its own `127.0.0.1`, and nothing is listening on it because nothing is running inside the container on that port. 

The fix depends on your OS and situation: 
    
    
    # On Mac and Windows — Docker Desktop injects this magic hostname:
    http://host.docker.internal:8080
    
    # On Linux (Docker Engine, no Desktop) — two options:
    
    # Option 1: Use the gateway IP directly
    # (run this from inside the container to find it)
    ip route | awk '/default/ { print $3 }'
    # Usually 172.17.0.1 for the default bridge
    
    # Option 2: Add the alias explicitly in docker-compose.yml
    extra_hosts:
      - "host.docker.internal:host-gateway"
    
    # Option 3: Use host networking entirely
    docker run --network host my-container
    # Now localhost IS your host's localhost
    # (Linux only — Mac and Windows don't support host networking)

⚠️ Linux + AI Stacks

If you're building on Linux (which you probably are, given the GPU), the `host.docker.internal` hostname doesn't exist by default. Add the `extra_hosts: host-gateway` trick to every service in your `compose.yml` that needs to reach the host. Yes, every one. 

In practice: when building the Nebulus stack, every container that needed to talk to the host-side inference server had to get this treatment. Missed it once in `nebulus-gantry`. Spent an embarrassing amount of time with `curl` before noticing the compose file was clean on Mac but broken on the Linux deployment. 

Lie #2

## Containers on the Same Host Can Talk to Each Other

Well — they can. But not the way you're probably thinking. 

By default, every `docker run` container goes onto the `bridge` network. Containers on the bridge can technically reach each other by IP, but here's the catch: the IPs are ephemeral. Every container gets a different address every time it starts. Hardcoding them is a recipe for intermittent failures. 

Docker Compose changes the game here. When you define services in a `compose.yml`, Compose automatically creates a shared network for all of them and registers each service by name as a DNS hostname. Your `tabby-api` service is reachable as `http://tabby-api:8080` from any other service in the same compose file. 
    
    
    # compose.yml — these services can find each other by name
    services:
      tabby-api:
        image: tabbyml/tabby
        ports:
          - "8080:8080"
    
      chromadb:
        image: chromadb/chroma
        ports:
          - "8000:8000"
    
      conductor:
        image: westailabs/nebulus-core
        environment:
          # Reference by service name, not localhost or IP
          INFERENCE_URL: http://tabby-api:8080
          VECTOR_DB_URL: http://chromadb:8000
        depends_on:
          - tabby-api
          - chromadb

This works because Compose creates a private network (by default named `<project>_default`) and every service on it gets a DNS entry matching its service name. The Docker daemon runs an embedded DNS server inside each container that resolves these names. 

Where it breaks down: cross-compose stacks. If your inference server is in one `compose.yml` and your orchestration layer is in another, they're on different networks by default and can't find each other by name. 
    
    
    # Solution: use an external named network
    # Create it once:
    docker network create nebulus-internal
    
    # In each compose.yml:
    networks:
      nebulus-internal:
        external: true
    
    services:
      tabby-api:
        networks:
          - nebulus-internal
    
      conductor:
        networks:
          - nebulus-internal

💡 AI Stack Pattern

For production AI workloads with separate repos per component (inference, orchestration, memory, API gateway), the external named network pattern is your friend. Define it once per environment, reference it everywhere. Services find each other by name across compose stacks. 

Lie #3

## Exposed Ports Are Just for External Access

This one's more of an omission than a lie, but it causes real confusion and real security problems. 

When you write `ports: - "8080:8080"` in Compose (or `-p 8080:8080` in Docker run), you're binding port 8080 on your _host_ to port 8080 in the container. The default binding is to `0.0.0.0` — meaning every network interface on your machine. Your LAN. Your VPN interface. Everything. 

If you're running a local inference server with no authentication (common during development), you just exposed it to your entire local network. Maybe your whole office. Maybe more, depending on your firewall situation. 
    
    
    # This binds to ALL interfaces — your LAN can reach it:
    ports:
      - "8080:8080"
    
    # This binds to localhost ONLY — only your machine can reach it:
    ports:
      - "127.0.0.1:8080:8080"
    
    # Explicit: bind to a specific interface (e.g., your internal NIC)
    ports:
      - "192.168.1.50:8080:8080"

For local AI development stacks, especially anything without authentication (TabbyAPI in development mode, raw ChromaDB, local Ollama behind Docker), locking to `127.0.0.1` is the right default. You can still reach it from the host, and internal containers can still reach it via the host gateway. You've just stopped broadcasting it to your network. 

⚠️ The GPU Server Risk

If you're running an inference server on a machine with real GPU capacity and you've port-published to `0.0.0.0`, anyone on your network can use your GPU. This isn't theoretical — it's happened on open dev networks. Add auth or lock the bind address. Both if you can. 

## The Mental Model That Actually Works

Here's how I think about Docker networking now, after all of it: 

  * **Inside a container:** You have your own network stack. Nothing from the host is visible unless you explicitly bridge it.
  * **Between containers (same Compose project):** Service names are DNS hostnames. Use them. Never hardcode IPs.
  * **Between containers (different Compose stacks):** Create a named external network. Join every relevant service to it.
  * **Container → Host:** `host.docker.internal` on Mac/Win. `extra_hosts: host-gateway` on Linux. Or `--network host` on Linux if you need full access.
  * **Host → Container:** Works via published ports (`ports:`). Lock to `127.0.0.1` unless you intentionally want LAN access.

Most multi-container AI stacks — the kind with an inference layer, a vector DB, an orchestration service, and an agent runtime — will hit all three of these lies at least once. Usually in the same afternoon. Usually when you're trying to demo something. 

The good news: once you've burned yourself, you don't forget. And none of it is magic — it's just a NAT table and a DNS server, both of which Docker manages for you if you tell it what you want. 

* * *

If you're building containerized AI infrastructure and want to avoid the 2 AM debugging sessions, start with `extra_hosts: host-gateway` in your compose files, named external networks for cross-stack communication, and `127.0.0.1` port binds for anything that doesn't need LAN exposure. Get these right up front and the rest usually follows. 

The infrastructure isn't the interesting part. Get it right so you can focus on what is.