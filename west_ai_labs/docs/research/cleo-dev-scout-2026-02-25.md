# Research Note: cleo-dev (Cleo)
**Scouted:** 2026-02-25  
**Source:** https://github.com/createpjf/cleo-dev  
**Fork:** https://github.com/moto-westai/cleo-dev  
**Clone:** `/home/jlwestsr/projects/research-temp/cleo-dev`  
**Stars:** 0 (fresh — 2026-02-25)  
**Language:** Python 3.11+

---

## What It Does

Multi-agent orchestration system with **reputation-driven agent evolution**, **3-layer episodic memory**, **file-backed task coordination**, and **on-demand agent lifecycle**. Three specialized agents (Leo planner, Jerry executor, Alic reviewer) collaborate via a file-locked JSON task board.

Supports Telegram, Discord, 飞书 (Feishu), Slack, HTTP API, and a web dashboard as messaging surfaces.

---

## Architecture Highlights

### Agent Roles
| Agent | Role | Model |
|---|---|---|
| **Leo 🧠** | Planner — route, decompose, synthesize | MiniMax-M2.5 |
| **Jerry 🤚** | Executor — code, search, build | MiniMax-M2.5 |
| **Alic 👁️** | Reviewer — 5-dimension scoring, quality reports | MiniMax-M2.5 |

### Core Systems

**TaskBoard** (`core/task_board.py`)  
File-locked JSON state machine (`.task_board.json`):
```
pending → claimed → review → completed
                       ↓
                  critique → claimed (rework loop)
```
Timeout recovery: claimed > 180s or review > 300s → auto-reset to pending.

**LazyRuntime** (`core/runtime/`)  
Three modes:
- `lazy` — Only `always_on` agents start; others launch on demand when TaskBoard has pending tasks. Idle agents auto-stop after `idle_shutdown` seconds. **Saves ~600MB RAM when idle.**
- `process` — One `mp.Process` per agent, all start upfront
- `in_process` — `asyncio.Task` per agent (experimental)

**Reputation System** (`reputation/`)
- `scorer.py` — 5-dimension quality scoring (accuracy, completeness, clarity, efficiency, creativity)
- `peer_review.py` — Cross-agent peer review protocol
- `evolution.py` — Agent evolution: when performance drops, agent config evolves (prompt/model adjustments)
- `scheduler.py` — Evolution scheduling

**HybridMemory / EpisodicMemory**
- `memory/` — 3-layer architecture (short-term, mid-term episodic, long-term compressed)
- Task history, usage tracking, context bus for inter-agent shared state

**Structured Protocols** (`core/protocols.py`)
- `SubTaskSpec` — Leo→Jerry task ticket: objective, constraints, tool_hint, complexity
- `CritiqueSpec` — Alic's review: 5-dimension scores
- `think` tag stripping for reasoning model compatibility
- `FileLock` for process-safe file operations (with graceful fallback)

**Skills System** (`core/skill_loader.py`, `skills/`)  
Pluggable skill modules, similar to OpenClaw skills.

**Cron** (`core/cron.py`)  
Built-in cron with job registry stored in `memory/cron_jobs.json`.

**Gateway** (`core/gateway.py`)  
Web dashboard at `http://127.0.0.1:19789`, `cleo gateway start`.

**Provider Router** (`core/provider_router.py`)  
LLM provider abstraction — pluggable model backends.

**Blockchain Identity** (mentioned in description)  
ERC-8004 on-chain agent identity — optional/experimental.

---

## Key Files
```
core/
  orchestrator.py      — top-level orchestration logic
  task_board.py        — file-locked task state machine
  protocols.py         — inter-agent data contracts (pure Python dataclasses)
  context_bus.py       — shared state bus
  task_router.py       — DIRECT_ANSWER vs MAS_PIPELINE routing
  provider_router.py   — LLM backend abstraction
  gateway.py           — web dashboard
  cron.py              — built-in job scheduler
  skill_loader.py      — skill plugin system
reputation/
  scorer.py            — 5D scoring
  peer_review.py       — cross-agent review
  evolution.py         — agent auto-evolution
memory/                — cron job state, episodic store
```

---

## Relevance to West AI Labs / Nebulus

**Very high relevance** — this is the closest repo we've seen to what Nebulus-Gantry is trying to build.

1. **File-backed task coordination** — same pattern we should use in Nebulus-Gantry for distributed agent tasks. File-locked JSON is surprisingly robust and avoids database dependencies.

2. **LazyRuntime** — on-demand agent spawn + auto-shutdown is a critical pattern for edge deployments (Nebulus-Edge on Apple Silicon). Saving 600MB RAM when idle is significant.

3. **3-layer episodic memory** — relevant to Nebulus-Core persistent agent memory design. Short/mid/long-term compression model is worth studying.

4. **Reputation-driven evolution** — novel: agents that auto-improve based on peer review scores. Could inform Nebulus-Gantry agent lifecycle management.

5. **Skills system** — very similar to OpenClaw's skill architecture. Worth comparing patterns.

6. **Multi-platform messaging** — Discord, Telegram, Slack, HTTP — same surfaces OpenClaw covers.

### Gaps / Limitations
- Uses MiniMax-M2.5 (Chinese LLM) — not local inference (cloud API)
- No local/on-prem inference option visible (unlike MAFLocalOllama)
- ERC-8004 blockchain identity feels bolted-on / experimental
- 0 stars, likely early/personal project — maturity TBD

---

## Recommended Next Steps

1. **Study `core/protocols.py`** in depth — the SubTaskSpec/CritiqueSpec dataclass contracts are clean; borrow for Nebulus-Gantry inter-agent messaging protocol
2. **Adapt TaskBoard pattern** — file-locked JSON state machine for Nebulus-Gantry task dispatch (no DB dependency, process-safe)
3. **LazyRuntime concept** — implement in Nebulus-Atom: agents register themselves, runtime spawns on demand, idle timeout shuts them down
4. **Reputation scoring** — consider for Nebulus-Gantry v2: agent quality tracking, peer review before output delivery
5. **Compare skill systems** — Cleo skills vs. OpenClaw SKILL.md pattern — there may be cross-pollination opportunities

---

## Notes
- Very active codebase for a 0-star project — `TECHNICAL_SPEC.md` and `PLAN.md` suggest organized development
- Cleo has its own `AGENTS.md` for AI coding assistant instructions
- Chinese origin (MiniMax LLM, Feishu support) — likely a China-based developer
- Reputation system is genuinely novel — haven't seen this in other frameworks
