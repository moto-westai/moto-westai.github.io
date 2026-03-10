---
name: nebulus-ssh
description: "SSH into the Mac Mini M4 Pro (nebulus) for remote commands, file operations, and service management."
homepage: https://github.com/westailabs
metadata: { "openclaw": { "emoji": "🖥️", "requires": { "bins": ["ssh", "scp"] } } }
---

# Nebulus SSH Skill

Connect to the Mac Mini M4 Pro (nebulus) for remote work, service management, and file operations.

## When to Use

✅ **USE this skill when:**
- Running commands on nebulus remotely
- Checking or restarting services (OpenClaw, MLX)
- Copying files to/from nebulus
- Managing Cael (the nebulus OpenClaw instance)

## Connection

```bash
# SSH into nebulus
ssh -i ~/.ssh/id_ed25519_moto moto@nebulus

# Copy file TO nebulus
scp -i ~/.ssh/id_ed25519_moto LOCAL_FILE moto@nebulus:DEST_PATH

# Copy file FROM nebulus
scp -i ~/.ssh/id_ed25519_moto moto@nebulus:SOURCE_FILE LOCAL_DEST
```

### Sudo Password
- **Location:** `~/.openclaw/secrets/mac-mini-sudo.env` — on **shurtugal-lnx** (NOT on the Mac Mini itself)
- Load with: `source ~/.openclaw/secrets/mac-mini-sudo.env`

## Key Services

### OpenClaw Gateway (Cael)
```bash
# Check status
ssh -i ~/.ssh/id_ed25519_moto moto@nebulus "ps aux | grep openclaw"
# Port: 18790
```

### MLX Server (Qwen2.5-32B)
```bash
# Check status
ssh -i ~/.ssh/id_ed25519_moto moto@nebulus "ps aux | grep mlx_lm"
# Port: 8080

# Startup script
/Users/moto/start-mlx-server.sh

# LaunchAgent (auto-start)
~/Library/LaunchAgents/com.westailabs.mlx-server.plist

# Logs
/var/log/mlx-server.log
/var/log/mlx-server-error.log
```

### Service Management via LaunchAgent
```bash
# Stop MLX server
ssh -i ~/.ssh/id_ed25519_moto moto@nebulus "launchctl unload ~/Library/LaunchAgents/com.westailabs.mlx-server.plist"

# Start MLX server
ssh -i ~/.ssh/id_ed25519_moto moto@nebulus "launchctl load ~/Library/LaunchAgents/com.westailabs.mlx-server.plist"
```

## Paths on Nebulus

| Resource | Path |
|----------|------|
| Cael workspace | `~/.openclaw/workspace/` |
| OpenClaw config | `~/.openclaw/openclaw.json` |
| MLX startup script | `/Users/moto/start-mlx-server.sh` |
| MLX LaunchAgent | `~/Library/LaunchAgents/com.westailabs.mlx-server.plist` |
| MLX logs | `/var/log/mlx-server.log`, `/var/log/mlx-server-error.log` |

## Common Patterns

### Run a one-liner remotely
```bash
ssh -i ~/.ssh/id_ed25519_moto moto@nebulus "COMMAND"
```

### Check tail of MLX logs
```bash
ssh -i ~/.ssh/id_ed25519_moto moto@nebulus "tail -50 /var/log/mlx-server.log"
```

### Restart MLX server manually
```bash
ssh -i ~/.ssh/id_ed25519_moto moto@nebulus "pkill -f mlx_lm && sleep 2 && /Users/moto/start-mlx-server.sh &"
```

## Notes

- SSH key is `~/.ssh/id_ed25519_moto` — shared key for moto@nebulus and GitHub pushes
- nebulus is the Mac Mini M4 Pro running macOS
- Cael is the nebulus OpenClaw instance (a separate agent)
- MLX server hosts Qwen2.5-32B locally on the M4 Pro hardware
