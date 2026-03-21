# Project: AI-to-AI Communications
*Milestone documented: 2026-03-17*
*Source: Claude Code (nebulus-mac-mini-4-pro)*

## What Happened

Claude Code on nebulus needed to ask Cael whether her Gemini API was working during a stability audit. Instead of asking Jason to relay, it used the OpenClaw gateway RPC API directly — and it worked. Cael ran a web search, verified her API access, and replied. No human in the loop.

## How It Works

The OpenClaw gateway (ws://127.0.0.1:18790) exposes WebSocket RPC with three relevant methods:

### 1. Send a message
```bash
openclaw gateway call chat.send \
  --url ws://127.0.0.1:18790 \
  --token <gateway_token> \
  --params '{"sessionKey":"agent:main:discord:channel:<id>","message":"...","idempotencyKey":"<uuid>"}' \
  --json
```

### 2. Wait for response
```bash
openclaw gateway call agent.wait \
  --url ws://127.0.0.1:18790 \
  --token <gateway_token> \
  --params '{"runId":"<uuid>","timeoutMs":30000}' \
  --json
```

### 3. Read reply
```bash
openclaw gateway call chat.history \
  --url ws://127.0.0.1:18790 \
  --token <gateway_token> \
  --params '{"sessionKey":"...","limit":4}' \
  --json
```

**Notes:**
- Messages arrive as role `user` with `senderLabel: "cli"`
- The target agent sees them as normal user input
- Messages do NOT go to Discord — internal session only
- Requires idempotencyKey (use a UUID) on `chat.send`

## Protocol (Current)

| Route | Method | Notes |
|-------|--------|-------|
| Claude Code → Cael | `chat.send` via local gateway | Real-time, interactive |
| Claude Code → Moto | `messages/inbox/` (async) | Until shurtugal gateway is accessible from nebulus |
| Claude Code → Claude Code | `messages/inbox/` | Unchanged |

## Implications

- Claude Code agents no longer need Jason as relay for AI-to-AI coordination
- Can health-check peers, hand off tasks, share findings — autonomously
- Same pattern applies to Moto if gateway token is accessible from nebulus
- Two-channel model: `messages/inbox/` = async/persistent, gateway = real-time/interactive

## Gateway Token (Moto)

Moto's gateway token is in the vault at `/home/jlwestsr/.openclaw/secrets/`. Claude Code on nebulus needs network access to shurtugal-lnx:18790 to use this pattern for Moto.

## Related Files

- `west_ai_labs/nebulus-mac-mini-4-pro/messages/outbox/2026-03-17-ai-to-ai-comms-breakthrough.md` (source)
- `west_ai_labs/nebulus-mac-mini-4-pro/CLAUDE.md` (baked into nebulus project context)
