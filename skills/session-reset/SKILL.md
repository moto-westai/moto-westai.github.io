---
name: session-reset
description: Reset an OpenClaw agent session for a specific channel so the next prompt starts fresh, picking up the latest .md config files. Use when an agent needs to reload its SOUL.md, AGENTS.md, HEARTBEAT.md, or other workspace files after a config change. Triggers on phrases like "reset your session", "reset Cael's session", "start fresh", "reload your config", or "reset the session for [channel]".
---

# Session Reset

Resets an OpenClaw session by archiving the current session file and removing the channel's entry from `sessions.json`. The next message received on that channel creates a fresh session, loading all current `.md` config files from disk.

## Sessions JSON Location

```
~/.openclaw/agents/<agentId>/sessions/sessions.json
```

For Moto (main agent on shurtugal-lnx): `~/.openclaw/agents/main/sessions/sessions.json`

## Session Key Format

```
agent:main:discord:channel:<channel_id>
```

Common channels:
- `#jlwestsr-office` → `agent:main:discord:channel:1475994576668852254`
- `#schmibb-office`  → `agent:main:discord:channel:1475997091791896657`
- `#cael-office`     → `agent:main:discord:channel:1476368504767905845`
- `#motos-office`    → `agent:main:discord:channel:1473772830419194001`

## Reset Steps

### 1. List sessions (optional — to find the right key)

```bash
python3 ~/.openclaw/workspace/skills/session-reset/scripts/reset_session.py \
  ~/.openclaw/agents/main/sessions/sessions.json --list
```

### 2. Reset a specific channel session

```bash
python3 ~/.openclaw/workspace/skills/session-reset/scripts/reset_session.py \
  ~/.openclaw/agents/main/sessions/sessions.json \
  "agent:main:discord:channel:<channel_id>"
```

### 3. Verify

Run `--list` again and confirm the key is gone. The next Discord message in that channel will start a fresh session.

## Notes

- **Self-reset caveat:** Resetting your own active session file is safe — the script archives it (`.jsonl.deleted.<timestamp>`) rather than deleting it, matching OpenClaw's own deletion pattern. The current turn completes normally; the fresh session loads on the next inbound message.
- **Cael's sessions:** Cael runs on nebulus. Her sessions.json is at `/Users/jlwestsr/.openclaw/agents/main/sessions/sessions.json` on nebulus, accessible via SSH. Moto can reset Cael's session only if SSH access to nebulus is configured.
- **Config change → reset → verify** is the standard workflow for behavioral changes to take effect.
