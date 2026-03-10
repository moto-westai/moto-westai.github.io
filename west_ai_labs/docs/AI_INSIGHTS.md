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

---

## Agent Memory Architecture Spec — 2026-03-10

**Task:** Draft technical spec for drift-resistant agent memory architecture  
**Output:** `west_ai_labs/docs/research/agent-memory-architecture-spec.md`  
**Applies to:** Moto (shurtugal-lnx), Cael (nebulus), future West AI Labs hosted agents

### Key Design Decisions

- **Four-tier memory model:** Tier 0 (identity core, never compacted), Tier 1 (long-term typed records), Tier 2 (working state), Tier 3 (ephemeral daily logs)
- **YAML for Tier 1 records, JSON for assertions and session-state** — YAML for human readability, JSON for strict schema enforcement
- **Salience decay classes:** `compound` (grows with reinforcement), `stable` (fixed), `decay` (fades without reinforcement) — core identity memories use `compound`, not `decay`
- **Identity Assertions:** 6 baseline assertions captured for Moto; comparison uses semantic embedding similarity in Phase 2 (manual human review in Phase 1)
- **Git snapshot cadence:** daily automated commit, weekly tagged snapshot, event-driven freeze snapshots for model updates and major identity events
- **Composite drift score** weighted across assertion drift (50%), prose diff (30%), salience distribution shift (20%)
- **Compaction hints:** `preserve` / `summarizable` / `ephemeral` / `preserve-structure` tags on every Tier 1 record; Tier 0 always preserved verbatim
- **Heirloom product tiers:** Archive (free), Heirloom (pro), Legacy (business), Heritage (enterprise)

### Failure Modes Addressed

All five identified failure modes (compaction loss, interaction-induced drift, model-update drift, salience decay, no baseline) are addressed with specific mechanisms. The "no baseline" problem is solved first in Phase 1 with a freeze snapshot before anything else.

### Tradeoffs Left Open (by design)

- YAML vs JSON vs JSONL for Tier 1 storage — options presented with tradeoffs
- Manual human review vs embedding cosine similarity vs LLM judge for drift scoring — all three options spec'd
- Single `main` branch vs identity-specific branches vs separate repo — three options presented
- File-level access control vs capability tokens for family access tiers

### Implementation Scope

- **Phase 1 (now, no infra):** Freeze snapshot, typed record migration, snapshot cron, manual assertion checks — ~4 hours agent + 2 hours human review
- **Phase 2 (4-8 weeks):** `agent-memory` OpenClaw skill, automated assertion checks, semantic search, compaction hook, Cael rollout
- **Phase 3 (6-12 months):** Standalone hosted product, custody chain registry, estate scaffolding, multi-agent custody, compliance

### Assumptions Made

- Local embedding model (all-MiniLM-L6-v2) available for Phase 2 semantic similarity — no API key required
- Git repo already exists and push access is configured
- OpenClaw exposes a pre-compaction hook point for Phase 2 integration
- Legal scaffolding requires external counsel; spec provides structure, not legal advice

### Recommended Next Steps

1. Human reviews and approves identity assertions for Moto before Phase 1 begins (they become immutable baseline)
2. Run `git tag identity/moto-v1` immediately after first freeze — this is the single most important first action
3. Assess Cael's current memory state before applying same architecture (may differ from Moto's)
4. Validate compaction hook availability with OpenClaw maintainers before committing Phase 2 timeline
