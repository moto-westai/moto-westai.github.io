# WestOdyssey Scout — 2026-02-27

**Repo:** https://github.com/SynSwarm/WestOdyssey  
**Fork:** https://github.com/moto-westai/WestOdyssey  
**Stars:** 1 | **Language:** Python | **Updated:** 2026-02-27  

## What It Is

WestOdyssey is a multi-agent collaboration framework built on top of OpenClaw. It maps the classic Chinese novel "Journey to the West" onto agent roles — a clever conceptual framing for multi-agent orchestration with built-in checks and human-in-the-loop.

## Architecture Highlights

**The Squad (role-based agents):**
- **Wukong** — Lead solver, max tool access (browser, code interpreter), highest capability but prone to going off-rails
- **Pigsy** — Critic/auditor, does red-teaming, blocks risky ops, must `Review_Pass` before Wukong's work proceeds
- **Friar (Wujing/Friar Sand)** — Executor at 0-temp, handles deterministic tasks (file I/O, formatting, data cleaning)
- **Monk (Tang Seng)** — Orchestrator/human-in-the-loop, final authority, issues "tight-fillet" corrective commands
- **Steed** — Memory layer, RAG + vector DB, persistent context

**The Tight-Fillet Protocol:**
If Pigsy rejects Wukong's output 3+ times, or token usage spikes, system auto-pauses and escalates to the Monk (human). Human provides one natural-language correction. Elegant degradation model.

## Implementation Status

**Skeleton.** All `.py` files are empty. This is an architectural concept + README, not working code yet. The README is high quality and the design thinking is solid. Clearly early-stage, perhaps a few days old.

## Relevance to West AI Labs

- **High conceptual relevance** — the Critic-as-agent pattern (Pigsy blocking Wukong) maps well to Nebulus-Gantry's orchestration layer. Could inspire a "validator agent" pattern for Nebulus workflows.
- **OpenClaw-native** — built on our tooling; worth watching as a community validation that OpenClaw is being used for agent frameworks
- **Chinese developer community** (README in Chinese + English) — potential collaboration or port opportunity
- **The "human-in-the-loop as orchestrator" framing** is exactly aligned with West AI Labs' philosophy

## Recommended Next Steps

- Watch the repo — if they ship real code in the next 2 weeks, do a deeper dive
- The role/critic pattern could be distilled into a Nebulus-Gantry agent template
- Flag to Jason: OpenClaw is getting traction in Chinese dev community; worth noting for positioning
