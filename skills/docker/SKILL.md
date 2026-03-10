---
name: docker
description: Manage Docker containers, images, volumes, networks, and Compose V2 stacks on Linux. Use when the user asks to build, run, inspect, troubleshoot, or manage Docker containers or docker compose services. Covers container lifecycle, logs, resource usage, compose up/down/restart, image management, and debugging failing containers.
---

# Docker Management

## Environment

- Docker Compose V2 (`docker compose`, not `docker-compose`)
- Linux host
- All commands use `docker` and `docker compose` CLI

## Common Operations

### Container Lifecycle

```bash
# List running (add -a for all)
docker ps

# Start/stop/restart
docker compose up -d [service]
docker compose down
docker compose restart [service]

# Rebuild and restart
docker compose up -d --build [service]
```

### Inspection & Debugging

```bash
# Logs (follow, tail)
docker compose logs -f --tail=100 [service]

# Shell into running container
docker exec -it <container> /bin/bash

# Inspect container details
docker inspect <container>

# Resource usage
docker stats --no-stream

# Check why a container exited
docker inspect --format='{{.State.ExitCode}} {{.State.Error}}' <container>
```

### Images & Cleanup

```bash
# List images
docker images

# Remove dangling images
docker image prune -f

# Full cleanup (stopped containers, unused networks, dangling images)
docker system prune -f

# Nuclear cleanup (includes unused images)
docker system prune -a -f
```

### Volumes & Networks

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect <volume>

# List networks
docker network ls
```

### Compose File Validation

```bash
docker compose config
```

## Troubleshooting Checklist

When a container won't start or keeps restarting:

1. Check logs: `docker compose logs <service>`
2. Check exit code: `docker inspect --format='{{.State.ExitCode}}' <container>`
3. Check resource limits: `docker stats --no-stream`
4. Validate compose file: `docker compose config`
5. Check port conflicts: `ss -tlnp | grep <port>`
6. Check volume mounts exist and have correct permissions

## Guidelines

- Always use `docker compose` (V2), never `docker-compose`
- Before destructive operations (prune, rm), confirm with the user
- When showing logs, default to `--tail=50` unless asked for more
- For GPU containers (NVIDIA), check `nvidia-smi` and `nvidia-ctk` availability
