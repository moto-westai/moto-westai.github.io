# West AI Labs Community Guides
## Gaming PC → AI Agent Setup Series

> Turn your gaming PC into a local AI powerhouse — no cloud, no subscriptions, no data leaving your house.

These guides follow Jr.'s journey: an old gaming PC, Ubuntu, and a lot of "wait, this actually works?" moments — ending with Hohenheim, an AI Dungeon Master that's been running D&D campaigns for months.

If he can do it, so can you.

---

## The Guides

| # | File | What It Covers |
|---|------|----------------|
| 01 | [guide-01-is-my-gpu-ready.md](./guide-01-is-my-gpu-ready.md) | VRAM requirements for 7B–70B models, which NVIDIA cards work, and your minimum specs |
| 02 | [guide-02-ubuntu-ai-setup.md](./guide-02-ubuntu-ai-setup.md) | Ubuntu install, NVIDIA drivers, CUDA toolkit, Docker with GPU passthrough, and Ollama |
| 03 | [guide-03-ollama-openclaw-quickstart.md](./guide-03-ollama-openclaw-quickstart.md) | Install OpenClaw, connect it to Ollama, start the Gateway, and have your first agent conversation |
| 04 | [guide-04-discord-integration.md](./guide-04-discord-integration.md) | Create a Discord bot, configure intents, add your token to OpenClaw, and pair your first channel |
| 05 | [guide-05-giving-your-agent-personality.md](./guide-05-giving-your-agent-personality.md) | SOUL.md and MEMORY.md explained plainly, example personality templates, and tips for making your agent feel like *yours* |

---

## Prerequisites

- An NVIDIA GPU (AMD technically works but isn't covered here)
- A computer you can install Ubuntu on (dual boot is fine)
- A Discord account
- Time and curiosity

---

## The Stack You'll Build

```
Discord ←→ OpenClaw Gateway ←→ Ollama ←→ Your GPU
               ↓
          SOUL.md + MEMORY.md
          (your agent's personality + memory)
```

Everything runs locally. Your conversations stay on your machine. The only thing that leaves is what you explicitly send to Discord.

---

## Questions?

Come find us in the West AI Labs Discord. Show us what you build. We want to meet your agent.

---

*West AI Labs Community | Updated Feb 2026*
