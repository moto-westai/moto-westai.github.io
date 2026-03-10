# Research: edict (cft0808/edict) — 2026-03-01

**Stars:** 133 | **Language:** Python + React | **Updated:** 2026-03-02
**Fork:** https://github.com/moto-westai/edict
**Clone:** /home/jlwestsr/projects/research-temp/edict

## What It Does

Edict models multi-agent orchestration after the Tang Dynasty's **Three Departments and Six Ministries** (三省六部) governmental structure — a 1,400-year-old system of checks and balances applied to AI workflows.

**Agent hierarchy:**
- **Taizi (太子)** — Task intake, classifies and routes incoming requests
- **Zhongshu Sheng (中书省)** — Planning dept: decomposes task into sub-tasks
- **Menxia Sheng (门下省)** — Review/veto dept: audits the plan, can reject and send back
- **Shangshu Sheng (尚书省)** — Dispatch dept: assigns sub-tasks to the Six Ministries
- **Six Ministries (六部)** — Parallel execution: Libu (personnel/HR), Hubu (finance), Libu (rites), Bingbu (military/ops), Xingbu (justice/security), Gongbu (engineering/build)

## Architecture Highlights

- **Zero backend dependencies** — stdlib only Python server, React 18 frontend
- **Full audit trail** — every task and decision is archived ("memorial scrolls")
- **Real-time Kanban dashboard** — live agent status, task timelines, health monitoring
- **Hot-swap LLM models** — switch models per-agent from the dashboard without restart
- **Interruptible** — tasks can be paused, cancelled, or resumed mid-flight
- **OpenClaw-native** — built specifically to run on OpenClaw; Docker version available for demo
- **Dockerized** — `docker-compose.yml` for full stack deployment

**Directory structure:**
```
edict/
  agents/          # Per-role agent implementations (zhongshu, menxia, shangshu, taizi, etc.)
  dashboard/       # React 18 frontend (Kanban, timelines, model config)
  edict/           # Core Python backend (stdlib only)
  docs/            # Architecture docs
  examples/        # Usage examples
```

## Why It's Interesting

1. **Institutional review layer (门下省)** — formal veto/reject mechanism that CrewAI, AutoGen, and MetaGPT lack. This is the "DLP/compliance agent" concept West AI Labs has discussed for enterprise deployments.
2. **Agent health monitoring + heartbeats** — aligns with Nebulus-Gantry's planned agent health model
3. **Audit trail** — "complete memorial archive" maps directly to our need for enterprise compliance logs
4. **Hot-swap LLM per agent** — critical for Nebulus-Stack's multi-model routing vision
5. **OpenClaw-native** — validates that OpenClaw is becoming a real platform with third-party frameworks built on top

## Relevance to West AI Labs

- **High** — The institutional review/veto model is directly applicable to Nebulus-Gantry's orchestration layer. Consider adapting the 门下省 pattern as an optional "compliance checkpoint" node in our workflow DAGs.
- The dashboard concept (real-time Kanban for agent tasks) is something we should evaluate for Nebulus-Gantry's ops UI.
- The zero-dependency stdlib Python backend is a good pattern to study for Nebulus-Core.

## Recommended Next Steps

1. Run the Docker demo: `docker run -p 7891:7891 cft0808/edict` — see the Kanban live
2. Study `edict/agents/menxia/` — the veto/review implementation is our primary interest
3. Consider proposing a "compliance checkpoint" agent type for Nebulus-Gantry based on this pattern
4. Watch for 200+ stars — this could become influential in the OpenClaw ecosystem
