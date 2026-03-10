# Cael Migration Plan — nebulus → shurtugal-lnx Docker Container

## Overview
Move Cael from Mac Mini (nebulus) LaunchDaemon to a Docker container on shurtugal-lnx.
Use Anthropic OAuth (same as Moto) to fix the provider auth issue.

## What We Have
- ✅ Cael's workspace files copied to: `/home/jlwestsr/projects/cael-workspace/workspace/`
- ✅ SOUL.md, MEMORY.md (if exists), IDENTITY.md, HEARTBEAT.md, AGENTS.md, USER.md, TOOLS.md
- ✅ `openclaw:local` Docker image already on shurtugal-lnx
- ✅ Cael's Discord channel: #cael-office (ID: 1476368504767905845)
- ✅ Cael's SOUL.md intact — she's Cael, not Moto, knows Jason, has her own voice

## Port Assignment
- Moto uses: 18789 (gateway), 18790 (bridge)
- Cael will use: **18791** (gateway), **18792** (bridge)

## Setup Steps

### 1. Create Cael's config directory structure
```bash
mkdir -p /home/jlwestsr/projects/cael-workspace/agents/main/agent
mkdir -p /home/jlwestsr/projects/cael-workspace/agents/main/sessions
mkdir -p /home/jlwestsr/projects/cael-workspace/secrets
```

### 2. Copy Anthropic auth from Moto
```bash
cp ~/.openclaw/agents/main/agent/auth-profiles.json \
   /home/jlwestsr/projects/cael-workspace/agents/main/agent/auth-profiles.json
```

### 3. Create .env file
```
OPENCLAW_GATEWAY_TOKEN=<generate: openssl rand -hex 32>
CLAUDE_AI_SESSION_KEY=<from ~/.openclaw/openclaw.env>
CLAUDE_WEB_SESSION_KEY=<from ~/.openclaw/openclaw.env>
OPENCLAW_CONFIG_DIR=/home/jlwestsr/projects/cael-workspace
OPENCLAW_WORKSPACE_DIR=/home/jlwestsr/projects/cael-workspace/workspace
OPENCLAW_GATEWAY_PORT=127.0.0.1:18791
OPENCLAW_BRIDGE_PORT=127.0.0.1:18792
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_IMAGE=openclaw:local
```

### 4. Create docker-compose.yml
```yaml
services:
  cael-gateway:
    image: ${OPENCLAW_IMAGE:-openclaw:local}
    container_name: cael-gateway
    environment:
      HOME: /home/node
      TERM: xterm-256color
      OPENCLAW_GATEWAY_TOKEN: ${OPENCLAW_GATEWAY_TOKEN}
      CLAUDE_AI_SESSION_KEY: ${CLAUDE_AI_SESSION_KEY}
      CLAUDE_WEB_SESSION_KEY: ${CLAUDE_WEB_SESSION_KEY}
    volumes:
      - ${OPENCLAW_CONFIG_DIR}:/home/node/.openclaw
      - ${OPENCLAW_WORKSPACE_DIR}:/home/node/.openclaw/workspace
    ports:
      - "${OPENCLAW_GATEWAY_PORT:-127.0.0.1:18791}:18789"
      - "${OPENCLAW_BRIDGE_PORT:-127.0.0.1:18792}:18790"
    init: true
    restart: unless-stopped
    command:
      ["node", "dist/index.js", "gateway", "--bind", "lan", "--port", "18789"]
```

### 5. Configure model (Anthropic claude-sonnet)
Create `/home/jlwestsr/projects/cael-workspace/agents/main/agent/models.json`
pointing to anthropic/claude-sonnet-4-6

### 6. Configure Discord channel
Cael needs her openclaw.yaml to include the Discord channel config for #cael-office (1476368504767905845)
and the West AI Labs guild (1473761760115953738).

### 7. Start and pair
```bash
cd /home/jlwestsr/projects/cael-workspace
docker compose up -d
# Then run pairing: openclaw pairing new discord
# Approve in Discord
```

## Status
- [ ] Config directory created
- [ ] Auth copied
- [ ] .env written
- [ ] docker-compose.yml written
- [ ] Model configured
- [ ] Discord channel configured
- [ ] Container started
- [ ] Discord paired
- [ ] Cael online and responding

## Awaiting Jason Approval Before Execution
