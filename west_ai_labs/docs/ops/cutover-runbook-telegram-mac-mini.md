# Cutover Runbook: Telegram → Mac Mini (nebulus)
**Date:** 2026-02-21  
**Goal:** Move Telegram to Mac Mini (Opus), keep Discord on shurtugal (Sonnet)  
**Status:** STAGED — waiting for Jason at desk

---

## Architecture After Cutover

| Channel   | Host        | Gateway Port | Model  |
|-----------|-------------|--------------|--------|
| Telegram  | nebulus (Mac Mini M4 Pro) | 18790 | claude-opus-4-6 |
| Discord   | shurtugal-lnx | 18789 | claude-sonnet-4-6 |

---

## Pre-Cutover Checklist

- [ ] Jason is at desk with terminal access to both machines
- [ ] Both gateways currently running (`openclaw gateway status` on each)
- [ ] Rollback commands noted below and ready to paste
- [ ] No active critical conversations in flight (Jr, etc.)

---

## Step 1 — Verify Mac Mini Gateway is Running

```bash
ssh -i ~/.ssh/id_ed25519_moto moto@nebulus "openclaw gateway status"
# Expected: running on port 18790
```

If not running:
```bash
ssh -i ~/.ssh/id_ed25519_moto moto@nebulus "openclaw gateway start"
```

---

## Step 2 — Add Telegram to Mac Mini Config

On **shurtugal**, run:
```bash
ssh -i ~/.ssh/id_ed25519_moto moto@nebulus "cat ~/.openclaw/openclaw.json" > /tmp/nebulus-config-backup.json
```

The Telegram bot token from shurtugal:
```
7783219013:AAEhV3jZ7SIPTimGFEl0hM6sTljwiXLNGQ4
```

Add to Mac Mini's `~/.openclaw/openclaw.json` under `channels`:
```json
"channels": {
  "telegram": {
    "enabled": true,
    "dmPolicy": "pairing",
    "botToken": "7783219013:AAEhV3jZ7SIPTimGFEl0hM6sTljwiXLNGQ4",
    "groupPolicy": "allowlist",
    "streamMode": "partial",
    "actions": {
      "reactions": true,
      "sendMessage": true,
      "deleteMessage": true,
      "sticker": true
    }
  }
}
```

Also set the agent model to Opus:
```json
"agents": {
  "defaults": {
    "model": {
      "primary": "anthropic/claude-opus-4-6"
    }
  }
}
```

---

## Step 3 — Add Workspace Files to Mac Mini

Mac Mini needs identity/memory files. Sync from shurtugal:
```bash
rsync -av --progress \
  -e "ssh -i ~/.ssh/id_ed25519_moto" \
  /home/jlwestsr/.openclaw/workspace/SOUL.md \
  /home/jlwestsr/.openclaw/workspace/AGENTS.md \
  /home/jlwestsr/.openclaw/workspace/IDENTITY.md \
  /home/jlwestsr/.openclaw/workspace/USER.md \
  /home/jlwestsr/.openclaw/workspace/TOOLS.md \
  /home/jlwestsr/.openclaw/workspace/HEARTBEAT.md \
  /home/jlwestsr/.openclaw/workspace/MEMORY.md \
  moto@nebulus:/Users/moto/.openclaw/workspace/
```

Also sync memory directory:
```bash
rsync -av --progress \
  -e "ssh -i ~/.ssh/id_ed25519_moto" \
  /home/jlwestsr/.openclaw/workspace/memory/ \
  moto@nebulus:/Users/moto/.openclaw/workspace/memory/
```

---

## Step 4 — Disable Telegram on Shurtugal

Edit `/home/jlwestsr/.openclaw/openclaw.json` — change Telegram enabled to false:
```json
"channels": {
  "telegram": {
    "enabled": false,
    ...
  }
}
```

Also ensure Discord is set to use Sonnet by default. Add to `agents.defaults`:
```json
"model": {
  "primary": "anthropic/claude-sonnet-4-6"
}
```

---

## Step 5 — Restart Both Gateways (ORDER MATTERS)

**First — restart Mac Mini** (starts Telegram listener):
```bash
ssh -i ~/.ssh/id_ed25519_moto moto@nebulus "openclaw gateway restart"
```

Wait 10 seconds, verify Telegram connects by sending `/status` on Telegram.

**Then — restart shurtugal** (drops Telegram, keeps Discord):
```bash
openclaw gateway restart
# ⚠️ This will briefly interrupt this session
```

---

## Step 6 — Verification

- [ ] Send a Telegram message — should get response from Mac Mini (check via `hostname` or model confirmation)
- [ ] Send a Discord message — should get response from shurtugal
- [ ] Run `/status` on both channels to confirm correct models

---

## Rollback Plan

### If Mac Mini Telegram fails:

**On shurtugal:**
```bash
# Re-enable Telegram in config
# Edit ~/.openclaw/openclaw.json → channels.telegram.enabled = true
openclaw gateway restart
```

**Restore shurtugal config from backup:**
```bash
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
openclaw gateway restart
```

### If shurtugal gateway fails to come back:
```bash
# From any machine on LAN or direct console:
ssh jlwestsr@shurtugal-lnx
cd /home/jlwestsr/.openclaw/workspace/openclaw-fork
node dist/index.js gateway start
```

---

## Config Backup Locations

- Shurtugal backup: `~/.openclaw/openclaw.json.bak` (auto-created by OpenClaw)
- Manual backup: `~/.openclaw/openclaw.json.bak.4` (most recent pre-cutover)
- Mac Mini backup: `/tmp/nebulus-config-backup.json` (created in Step 2)

---

## Notes

- Telegram bot token can only be active on ONE gateway at a time — Telegram will disconnect from shurtugal automatically when Mac Mini connects
- The Mac Mini gateway token: `296fc506061a558def1aa7418f48f938317dd47f530e0312`
- Mac Mini gateway port: 18790 (LAN accessible at 192.168.4.30:18790)
- Pairing codes will need to be re-approved on Mac Mini for Jason + any other paired users

---

*Runbook prepared by Moto — 2026-02-21 07:54 CST*
