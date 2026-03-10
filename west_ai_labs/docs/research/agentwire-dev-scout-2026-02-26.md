# agentwire-dev — Scout Note
**Date:** 2026-02-26  
**Source:** https://github.com/dotdevdotdev/agentwire-dev  
**Fork:** https://github.com/moto-westai/agentwire-dev  
**Stars:** (new/growing)  
**Last Updated:** 2026-02-26

## What It Does
Push-to-talk voice control for Claude Code (and other AI coding assistants) running in tmux. WebSocket portal bridges phone/tablet to tmux session. Works over local network. Also has Telegram bridge for remote access.

## Architecture Highlights

### Core Flow
```
Phone → AgentWire Portal (WebSocket) → tmux pane → Claude Code
```
- Hold button to speak, release sends STT result as typed text to tmux
- Watch agent work in real-time via portal UI
- TTS reads responses back

### Components
- `portal` — WebSocket server + web UI (HTTPS self-signed)
- `pane_manager.py` — tmux pane orchestration
- `network.py` — local network discovery
- `bridges/telegram.py` — Telegram integration for remote SSH access
- `stt/` — pluggable STT backends: Whisper, WhisperKit (Apple Silicon), server backend
- `voices/` — TTS voice samples (Lisa, Jessica, Darren, May + default)
- `roles/` — agent role definition files (markdown)

### Multi-Agent
- Manage multiple projects/tmux sessions simultaneously from one portal
- Each session is a separate tmux pane with independent agent

### Install
- `pip install agentwire-dev`
- Requires: tmux, ffmpeg, Python 3.10+, Claude Code

## Relevance to West AI Labs
**MEDIUM-HIGH.** Direct overlap with Nebulus-Edge use case — Jason runs AI agents locally, wants voice/remote control. Key intersections:
- **Voice → tmux → Claude Code** is exactly the pattern for hands-free Nebulus workflows
- **Telegram bridge** matches Moto's existing Telegram connectivity — could enable "talk to Moto from anywhere" for Jason
- STT backend is pluggable — can hook into local Whisper on Nebulus-Prime
- The portal concept (WebRTC/WebSocket secure UI for tmux) is worth stealing for Nebulus-Gantry's management interface

## Recommended Next Steps
1. **Test voice → Moto workflow** — try `agentwire init` on shurtugal-lnx and see if push-to-talk into a Moto tmux session works
2. **Eval Telegram bridge** — could extend Jason's "talk to Moto" anywhere use case beyond Discord
3. **Watch star trajectory** — this is filling a genuine UX gap, likely to grow fast
4. **Heavy (82MB clone)** — includes voice sample files; note this when cleaning research-temp
