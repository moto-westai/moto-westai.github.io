# Bare Metal Migration Plan: OpenClaw Container → shurtugal-lnx Host

> **Author:** Moto | **Created:** 2026-02-17 | **Status:** Ready for Review
> **Target:** Move OpenClaw from Docker container to native install on shurtugal-lnx (Ubuntu 24.04)

---

## Why Migrate?

- **Direct hardware access:** Audio input, camera, USB devices (Moto sensory upgrade)
- **No Docker overhead:** Faster disk I/O, no bind-mount permission headaches
- **Persistent state:** No more losing files to container rebuilds
- **Full OS access:** systemd services, cron, networking, package management
- **Git operations:** Native SSH keys, no credential relay issues

## Current State (Container)

| Component | Location | Size |
|---|---|---|
| Config | `/home/jlwestsr/.openclaw/openclaw.json` | ~3KB |
| Workspace | `/home/jlwestsr/.openclaw/workspace/` | ~2.3GB |
| Credentials | `/home/jlwestsr/.openclaw/credentials/` | API keys, tokens |
| Memory (LanceDB) | `/home/jlwestsr/.openclaw/memory/` | Vector embeddings |
| Cron jobs | `/home/jlwestsr/.openclaw/cron/` | Scheduled tasks |
| Device pairings | `/home/jlwestsr/.openclaw/devices/` | Node identities |
| Telegram state | `/home/jlwestsr/.openclaw/telegram/` | Chat mappings |
| Session data | `/home/jlwestsr/.openclaw/agents/`, `subagents/` | Session history |
| Identity | `/home/jlwestsr/.openclaw/identity/` | Ed25519 keys |
| Media cache | `/home/jlwestsr/.openclaw/media/` | Downloaded media |
| OpenClaw fork | `workspace/openclaw-fork/` | Git repo (~1.5GB) |
| Git credentials | `~/.git-credentials` | GitHub PAT |
| Env file | `/home/jlwestsr/.openclaw/openclaw.env` | Environment vars |

## Pre-Migration Checklist

### 1. Backup Everything (on host, before touching anything)
```bash
# From shurtugal-lnx host
BACKUP_DIR="/home/jlwestsr/openclaw-backup-$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Copy the entire .openclaw directory from the container
docker cp openclaw-openclaw-gateway-1:/home/jlwestsr/.openclaw "$BACKUP_DIR/dot-openclaw"

# Also grab home directory dotfiles
docker cp openclaw-openclaw-gateway-1:/home/node/.git-credentials "$BACKUP_DIR/git-credentials" 2>/dev/null
docker cp openclaw-openclaw-gateway-1:/home/node/.gitconfig "$BACKUP_DIR/gitconfig" 2>/dev/null

# Verify backup integrity
du -sh "$BACKUP_DIR"
find "$BACKUP_DIR" -name "*.json" | head -20
ls -la "$BACKUP_DIR/dot-openclaw/openclaw.json"
```

### 2. Record Current State
```bash
# Inside container before shutdown
openclaw status > /tmp/openclaw-status-pre.txt
openclaw gateway status >> /tmp/openclaw-status-pre.txt

# List cron jobs
# (capture from gateway API or config)

# List paired devices
ls -la /home/jlwestsr/.openclaw/devices/

# Git branch state
cd /home/jlwestsr/.openclaw/workspace/openclaw-fork && git status && git log --oneline -5
```

### 3. Verify Host Prerequisites
```bash
# On shurtugal-lnx (bare metal)
node --version    # Need v20+ (v24.12.0 currently in container)
npm --version
git --version
python3 --version  # For any Python-based skills

# Check disk space
df -h /home/jlwestsr/
```

## Migration Steps

### Step 1: Install OpenClaw on Host
```bash
# On shurtugal-lnx as jlwestsr
curl -fsSL https://get.openclaw.ai | bash
# OR from the fork:
cd ~/openclaw-fork
npm install
npm link
```

### Step 2: Stop Container
```bash
docker compose down  # or docker stop openclaw-openclaw-gateway-1
```

### Step 3: Restore Data
```bash
BACKUP_DIR="/home/jlwestsr/openclaw-backup-YYYYMMDD"

# The .openclaw directory should land at ~/.openclaw
# If openclaw install created a fresh one, merge carefully:
cp -a "$BACKUP_DIR/dot-openclaw/openclaw.json" ~/.openclaw/openclaw.json
cp -a "$BACKUP_DIR/dot-openclaw/openclaw.env" ~/.openclaw/openclaw.env
cp -a "$BACKUP_DIR/dot-openclaw/credentials/" ~/.openclaw/credentials/
cp -a "$BACKUP_DIR/dot-openclaw/identity/" ~/.openclaw/identity/
cp -a "$BACKUP_DIR/dot-openclaw/devices/" ~/.openclaw/devices/
cp -a "$BACKUP_DIR/dot-openclaw/memory/" ~/.openclaw/memory/
cp -a "$BACKUP_DIR/dot-openclaw/cron/" ~/.openclaw/cron/
cp -a "$BACKUP_DIR/dot-openclaw/telegram/" ~/.openclaw/telegram/
cp -a "$BACKUP_DIR/dot-openclaw/agents/" ~/.openclaw/agents/
cp -a "$BACKUP_DIR/dot-openclaw/subagents/" ~/.openclaw/subagents/
cp -a "$BACKUP_DIR/dot-openclaw/media/" ~/.openclaw/media/

# Workspace (biggest piece — ~2.3GB)
cp -a "$BACKUP_DIR/dot-openclaw/workspace/" ~/.openclaw/workspace/

# Git credentials
cp "$BACKUP_DIR/git-credentials" ~/.git-credentials
chmod 600 ~/.git-credentials
```

### Step 4: Update Config Paths
The config references `/home/jlwestsr/.openclaw/workspace` which should already be correct on the host since we're using the same user. Verify:
```bash
grep -r "/home/node/" ~/.openclaw/openclaw.json  # Should find nothing
grep -r "workspace" ~/.openclaw/openclaw.json     # Should show correct path
```

If the container used `/home/node/`, update paths:
```bash
sed -i 's|/home/node/|/home/jlwestsr/|g' ~/.openclaw/openclaw.json
```

### Step 5: Update Gateway Bind
Container used `"bind": "lan"`. On bare metal this is fine, but verify:
```json
"gateway": {
  "port": 18789,
  "mode": "local",
  "bind": "lan"
}
```

### Step 6: Start & Verify
```bash
openclaw gateway start

# Verify
openclaw status
openclaw gateway status

# Test Telegram
# Send a test message from Telegram — should respond
```

### Step 7: Set Up systemd Service
```bash
# Create service file
sudo tee /etc/systemd/system/openclaw.service << 'EOF'
[Unit]
Description=OpenClaw Gateway
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=jlwestsr
WorkingDirectory=/home/jlwestsr
ExecStart=/usr/local/bin/openclaw gateway start --foreground
Restart=on-failure
RestartSec=10
Environment=HOME=/home/jlwestsr

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable openclaw
sudo systemctl start openclaw
```

### Step 8: Disable Docker Container Auto-Start
```bash
# Prevent the old container from starting on reboot
cd /path/to/docker-compose
docker compose down
# Or remove the restart policy
```

## Post-Migration Verification

| Check | Command | Expected |
|---|---|---|
| Gateway running | `openclaw status` | Running, healthy |
| Telegram works | Send message | Bot responds |
| Memory intact | Search for known memory | Returns results |
| Cron jobs active | Check cron list | All jobs present |
| Workspace files | `ls ~/.openclaw/workspace/SOUL.md` | File exists |
| Git repo clean | `cd workspace/openclaw-fork && git status` | Clean, correct branch |
| Device pairings | Check nodes | Devices listed |
| Audio/camera | `arecord -l` / `v4l2-ctl --list-devices` | Hardware detected |

## Zero Data Loss Checklist

- [ ] `openclaw.json` (config with all settings)
- [ ] `openclaw.env` (environment variables)
- [ ] `credentials/` (API keys — Anthropic, Brave, OpenAI, etc.)
- [ ] `identity/` (Ed25519 device keys — CRITICAL, cannot regenerate without re-pairing)
- [ ] `devices/` (node pairings)
- [ ] `memory/` (LanceDB vector store)
- [ ] `cron/` (scheduled jobs)
- [ ] `telegram/` (chat state, message IDs)
- [ ] `agents/` + `subagents/` (session history)
- [ ] `media/` (cached files)
- [ ] `workspace/` (all workspace files — SOUL.md, MEMORY.md, skills, openclaw-fork, west_ai_labs)
- [ ] `~/.git-credentials` (GitHub PAT)
- [ ] `exec-approvals.json` (tool approval state)
- [ ] `builtin-skills/` (may be regenerated, but copy for safety)

## Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Identity key mismatch | Devices won't connect | Copy `identity/` exactly; re-pair if needed |
| Path differences | Config breaks | Verify all paths; sed if needed |
| Missing Node.js version | Won't start | Install matching Node v24 via nvm |
| Permission issues | Can't read/write | `chown -R jlwestsr:jlwestsr ~/.openclaw` |
| LanceDB version mismatch | Memory search fails | Install same npm deps as container |
| Telegram webhook conflict | Dual responses | Stop container BEFORE starting bare metal |

## Rollback Plan

If anything goes wrong:
```bash
# Stop bare metal
openclaw gateway stop
sudo systemctl stop openclaw

# Restart container
docker compose up -d

# Container has bind mount — should resume with original state
```

## New Capabilities After Migration

Once on bare metal, Jason can set up:
1. **Audio input** — USB microphone for voice interaction
2. **Camera** — USB webcam for visual awareness
3. **Local network scanning** — Direct access to LAN
4. **GPU access** — Direct NVIDIA driver access (if needed)
5. **systemd integration** — Proper service management
6. **Full crontab** — OS-level scheduling alongside OpenClaw cron

---

*This plan assumes the container's bind-mounted `.openclaw` directory is at the same path on the host. If the Docker setup uses a different host path, adjust the backup commands accordingly.*
