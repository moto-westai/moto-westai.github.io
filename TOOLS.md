# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## TTS / Voice

- **Engine:** ElevenLabs (Creator/Pro tier, 110K chars/month)
- **CLI:** `sag` (brew: steipete/tap/sag)
- **Moto's voice:** Charlie — Deep, Confident, Energetic (ID: `IKne3meq5aSn9XLyUdCD`)
- **Key env:** `ELEVENLABS_API_KEY` in `~/.openclaw/openclaw.env`
- **Usage:** `sag speak -v "Charlie" -o /tmp/output.mp3 "text"`

## Examples

```markdown
### Cameras

- (none configured yet)

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: Charlie (deep, confident, energetic)
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
