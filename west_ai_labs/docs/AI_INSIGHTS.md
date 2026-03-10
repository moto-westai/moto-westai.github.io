# AI_INSIGHTS.md — West AI Labs Docs

Change control log for AI-generated and AI-assisted work in this project.

---

## 2026-02-27 — Community Guide Series: Gaming PC → AI Agent Setup

**Agent:** Moto (subagent, depth 1)
**Task:** Write a 5-part beginner guide series for the West AI Labs Discord community

### What Was Created

New directory: `docs/community/`

| File | Content |
|------|---------|
| `guide-01-is-my-gpu-ready.md` | VRAM requirements table (3B–70B), GPU compatibility list, CPU fallback notes |
| `guide-02-ubuntu-ai-setup.md` | Full Ubuntu AI stack: drivers → CUDA → Docker → NVIDIA Container Toolkit → Ollama |
| `guide-03-ollama-openclaw-quickstart.md` | Node.js install → OpenClaw install → Ollama connection → Gateway → first chat |
| `guide-04-discord-integration.md` | Discord Developer Portal walkthrough, intents, bot token, pairing flow, channel strategy |
| `guide-05-giving-your-agent-personality.md` | SOUL.md/MEMORY.md explanation, 3 example personality templates, tips for character depth |
| `README.md` | Series index with one-line descriptions and stack diagram |

### Design Decisions

- **Tone:** Friendly and practical, assumes gamer audience with zero Linux/AI experience
- **Jr.'s journey** used as a recurring proof point (old gaming PC → Ubuntu → Hohenheim running D&D campaigns)
- **AMD GPUs** acknowledged but explicitly out of scope — ROCm complexity would derail a beginner guide
- **Quantization** explained inline where first mentioned, not assumed knowledge
- **Security reminders** included in Guide 04 specifically around bot token handling
- CUDA install instructions provided for both Ubuntu 22.04 and 24.04 (noted in-guide)

### Assumptions Made

- Ollama version current as of Feb 2026 (one-liner installer via `install.sh`)
- OpenClaw commands (`openclaw init`, `openclaw gateway`, `openclaw chat`, etc.) reflect current CLI surface
- NVIDIA driver installation via `ubuntu-drivers` GUI path (most reliable for beginners)
- Docker install from official Docker apt repo (not Ubuntu's older snap version)

### Recommended Review

- Verify OpenClaw CLI command syntax matches current release before publishing
- Confirm `openclaw launch` / `ollama launch openclaw` syntax if that shortcut exists
- Consider adding a "what to do if your VRAM is full" note in Guide 01 for users with multiple GPU processes
