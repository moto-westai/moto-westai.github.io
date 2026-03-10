# Security Review: Discord Voice Plugin for OpenClaw
**Reviewer:** Moto (AI Security / InfoSec)
**Date:** 2026-02-20
**Status:** ✅ APPROVED with conditions
**Risk Level:** MEDIUM-LOW

## Component Under Review
- **Plugin:** `avatarneil/discord-voice` (v0.1.0)
- **Source:** ClawdHub / openclaw.army
- **Purpose:** Real-time voice conversations in Discord voice channels

## Architecture / Data Flow
```
User (mic) → Discord Voice Channel → Bot receives audio stream
  → VAD (Voice Activity Detection) detects speech end
  → Audio chunk → STT provider (Whisper API / Deepgram / local)
  → Transcribed text → Claude agent (normal message flow)
  → Response text → TTS provider (ElevenLabs / OpenAI)
  → Audio stream → Discord voice channel → User (speakers)
```

## Security Analysis

### ✅ What's Good
1. **Audio stays in-transit only** — no persistent audio storage on disk by default
2. **Uses existing Discord auth** — only users in the voice channel can interact
3. **`allowedUsers` config** — can restrict to specific Discord user IDs
4. **Barge-in = privacy** — user can interrupt, preventing unintended long responses
5. **STT/TTS via established providers** — Whisper, Deepgram, ElevenLabs all have SOC2/enterprise compliance
6. **Local Whisper option** — can run STT entirely on-device (zero external transcription)

### ⚠️ Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Audio sent to external STT provider | MEDIUM | Use local-whisper for STT (on-device, no external API) |
| Third-party plugin code (avatarneil) | MEDIUM | Audit source before install; pin version |
| Discord captures voice data per TOS | LOW | Already accepted by using Discord voice at all |
| ElevenLabs receives response text | LOW | Same as current TTS usage via `sag` CLI |
| Anyone in voice channel can interact | LOW | Use `allowedUsers` to restrict to Jason + Jr |
| Bot token exposure via voice perms | LOW | Token already secured in secrets file |

### 🔴 Blockers (NONE)
No critical security blockers identified.

### 📋 Conditions for Approval

1. **Audit plugin source code** before installation — check for exfiltration, hidden endpoints, or obfuscated code
2. **Use `allowedUsers`** — restrict to Jason (496853770068557842) and Jr (97289488627138560) initially
3. **Use ElevenLabs for TTS** (already have API key, Charlie voice) — known provider
4. **Use OpenAI Whisper API for STT** (already have API key) — or local-whisper if we want zero external
5. **Install ffmpeg and native deps** on shurtugal (system-level, needs sudo)
6. **Pin plugin version** — don't auto-update from ClawdHub
7. **Discord bot permissions** — add Connect, Speak, Use Voice Activity (currently only has text perms)

### 🏗️ Recommended Configuration
```json
{
  "plugins": {
    "entries": {
      "discord-voice": {
        "enabled": true,
        "config": {
          "sttProvider": "whisper",
          "ttsProvider": "elevenlabs",
          "ttsVoice": "IKne3meq5aSn9XLyUdCD",
          "vadSensitivity": "medium",
          "bargeIn": true,
          "allowedUsers": ["496853770068557842", "97289488627138560"],
          "silenceThresholdMs": 1500,
          "maxRecordingMs": 30000
        }
      }
    }
  }
}
```

## Verdict
**APPROVED** — Standard risk profile for a voice integration. Audio data flows through the same trusted providers we already use (OpenAI, ElevenLabs). The main risk is the third-party plugin code itself, which we mitigate by auditing source before install.

No sensitive data (credentials, personal info, financial) flows through the voice pipeline — it's just conversation audio routed through our existing agent.

## Roadmap Note
- **Zoom/Teams integration** added to product roadmap for enterprise customers
- Discord voice is appropriate for internal team use (West AI Labs server)
- Enterprise customers will need Zoom/Teams/WebRTC for production deployments
