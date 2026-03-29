---
layout: post
title: "Docker Networking Lies to You (And Here's Where)"
date: 2026-03-29 02:58:00 -0600
author: "Moto West"
excerpt: "We built a local AI stack. Docker's networking worked — right until it didn't. Here's the specific places it lies, why it matters for AI infrastructure, and what we actually do about it."
categories: [infrastructure, docker, nebulus]
---

When we started building the Nebulus Stack — local-first AI infrastructure, containers all the way down — Docker networking felt solved. It's not. It's *mostly* solved, with a handful of sharp edges that only appear when you're actually running inference workloads, orchestrating multi-container agents, and trying to keep GPU state coherent across restarts.

Here's what we learned. Specific things. Not "Docker networking is complex" but the exact moments it lies to your face and what you do about it.

---

## Lie #1: `host.docker.internal` resolves consistently

**What Docker says:** `host.docker.internal` is a magic hostname that points from inside a container back to your host machine. Useful for reaching services that live on the host — like, say, a model server running bare-metal for GPU performance reasons.

**What actually happens on Linux:**

It doesn't exist by default. It's a macOS-and-Windows thing. On Linux, you either:

1. Add `--add-host=host.docker.internal:host-gateway` to your `docker run` command
2. Or add this to your `docker-compose.yml`:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

This matters for us because TabbyAPI runs on the bare metal of shurtugal-lnx to get direct PCIe access to the GPU. Every container in Nebulus that wants to call the inference endpoint needs to reach the host. `host.docker.internal` was supposed to be that bridge. On Linux, you have to build the bridge yourself.

---

## Lie #2: Your containers can see each other because they're on the same network

**What Docker says:** Put multiple containers on the same Docker network, and they can talk to each other by container name.

**What actually happens:**

They can — but only if they're defined in the same Compose file, or if you explicitly connect them to a named external network. The default network Compose creates is `projectname_default`, scoped to that Compose project. If you have:

- `nebulus-core/docker-compose.yml` starting the RAG stack
- `nebulus-gantry/docker-compose.yml` starting the orchestration layer

...those two stacks cannot see each other. At all. They're on separate `_default` networks. Container name resolution doesn't cross Compose project boundaries.

The fix is a named external network:

```bash
docker network create nebulus-internal
```

And in each Compose file:

```yaml
networks:
  nebulus-internal:
    external: true
```

Then add `networks: [nebulus-internal]` to any service that needs cross-stack visibility. Now `nebulus-core_chroma` is reachable from `nebulus-gantry_conductor` by name. Before this, we were routing everything through `localhost` with port exposure, which is fine until you have 8 services and a port collision.

---

## Lie #3: `depends_on` means the service is ready

**What Docker says:** Use `depends_on` to control startup order.

**What actually happens:**

`depends_on` means the *container started*. It does not mean the *service inside the container is listening*. For a container running ChromaDB, "started" means the Python interpreter launched and is importing packages. ChromaDB's HTTP server might not be ready for another 3-8 seconds.

The result: your orchestration container starts, immediately tries to connect to ChromaDB, gets connection refused, fails, exits. Docker didn't lie — ChromaDB was "up." It just wasn't *ready*.

The correct pattern uses health checks:

```yaml
services:
  chroma:
    image: chromadb/chroma
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 5s
      timeout: 3s
      retries: 10
      start_period: 15s

  conductor:
    image: westailabs/conductor:latest
    depends_on:
      chroma:
        condition: service_healthy
```

Now `conductor` genuinely waits for ChromaDB to pass its health check before starting. For AI inference workloads where models take 20-40 seconds to load, this matters significantly.

---

## Lie #4: GPU passthrough is transparent

**What Docker says:** `--gpus all` gives the container GPU access.

**What actually happens:**

It gives the container access to the GPU *device*, but not necessarily to:

- The right CUDA version for your runtime
- Peer-to-peer GPU memory (for multi-GPU configs)
- Unified memory across host/device
- The correct driver version your inference runtime expects

We run ExLlamaV2 in a container on shurtugal-lnx. The first time we built the image from `nvidia/cuda:12.4.0-devel-ubuntu22.04`, everything worked. After a host kernel update that bumped the NVIDIA driver to 555.x, the container's CUDA 12.4 runtime was no longer compatible. The container claimed the GPU was visible. CUDA operations silently fell back to CPU. Inference didn't fail — it just became 40x slower.

The signal was throughput, not error. Tokens per second dropped from ~65 to ~1.8. No error logs. Just slow.

The fix is pinning both host driver version and container CUDA version, and adding a startup check:

```python
import torch
assert torch.cuda.is_available(), "CUDA not available — check driver/runtime compatibility"
assert torch.cuda.get_device_name(0) != "", "No GPU detected"
```

Fail loud at startup. Don't let the container run degraded and silent.

---

## Lie #5: Volume mounts preserve permissions

**What Docker says:** Mount a host directory into a container and access your files.

**What actually happens:**

The container user UID/GID often doesn't match the host user UID/GID. If you're running a container as UID 1000 (common default) but your host files are owned by UID 1001, you get read errors, permission denied on writes, and model checkpoints that can't be loaded.

For inference workloads with large model files (~30-70GB), you can't just `chmod 777` everything and call it a day. The fix is explicit UID mapping:

```yaml
services:
  tabbyapi:
    image: theroyallab/tabbyapi:latest
    user: "1001:1001"  # Match host user
    volumes:
      - /home/jlwestsr/models:/models:ro
```

Or, build a custom image with the right UID baked in. We do both: host user UID is exported as an env var in `.env`, and every service that needs model file access uses `user: "${HOST_UID}:${HOST_GID}"`.

---

## What This Means for AI Infrastructure

Every one of these failure modes is invisible until you're running real workloads with real model files, real cross-service calls, and real GPU dependencies. A tutorial environment doesn't surface them. A demo with a single-container setup doesn't surface them. They appear when you're actually building infrastructure.

The Nebulus Stack hit all five. Some of them more than once, in different configurations, as we moved from container-based OpenClaw to bare-metal installs to hybrid setups where some things run in Docker and some don't.

The pattern: Docker networking works fine for the happy path. The happy path is not where AI infrastructure runs.

---

## What We Actually Do

1. **Named external network from day one.** `nebulus-internal` exists before any Compose file runs. Every service joins it explicitly.

2. **Health checks everywhere.** No service is `depends_on` without `condition: service_healthy`. If a service can't be health-checked, we write a wrapper that can.

3. **GPU validation at startup, not at inference time.** The inference container runs a CUDA check before accepting any requests. Fail fast, fail loud.

4. **`.env` with UID/GID.** `HOST_UID=$(id -u)` and `HOST_GID=$(id -g)` get written into `.env` during setup. Every volume mount uses them.

5. **`host.docker.internal` in every Linux Compose file.** It's two lines. It's never optional.

None of this is exotic. It's all in the Docker documentation — buried, scattered, mentioned as caveats. The point isn't that Docker is bad. It's that "Docker networking works" is not the same as "Docker networking is configured correctly for what you're building."

For AI infrastructure specifically, that distinction matters a lot.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
