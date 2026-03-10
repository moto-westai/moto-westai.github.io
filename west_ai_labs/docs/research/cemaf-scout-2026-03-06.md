# CEMAF — Research Note
**Date:** 2026-03-06
**Repo:** drchinca/cemaf → fork: moto-westai/cemaf
**Clone:** /home/jlwestsr/projects/research-temp/cemaf
**Stars:** 0 (fresh, active dev)
**Language:** Python 3.11+
**License:** MIT

---

## What It Does

CEMAF (Context Engineering Multi-Agent Framework) is a **protocol-first, framework-agnostic** infrastructure layer for multi-agent AI systems. It attacks the hard plumbing problems: token budgets, context provenance, memory scoping, deterministic replay, and DAG orchestration — leaving the "business logic" to LangGraph/AutoGen/CrewAI.

The philosophy: own the hard infrastructure problems. Be pluggable everywhere else.

---

## Architecture Highlights

### Module Inventory (`src/cemaf/`)
- `agents/` — autonomous entity definitions
- `blueprint/` — declarative agent/workflow specs
- `cache/` — caching layer
- `citation/` — provenance and attribution tracking
- `config/` — env-based zero-config defaults
- `context/` — the core: token budgeting + context optimization
- `core/` — enums, types (AgentID, NodeID, RunID, SkillID, ToolID)
- `dag/` — runtime DAG composition
- `events/` — event bus
- `generation/` — LLM call abstraction
- `ingestion/` — data ingestion pipeline
- `llm/` — multi-provider LLM interface
- `mcp/` — Model Context Protocol integration
- `memory/` — scoped memory with TTL (base, protocols, factories)
- `moderation/` — content safety hooks
- `observability/` — metrics and tracing
- `orchestration/` — DAG executor, deep_agent, dependency resolver, planner, checkpointer
- `persistence/` — storage abstraction
- `replay/` — deterministic run recording + replay
- `resilience/` — retry, circuit breaker
- `retrieval/` — RAG / vector retrieval
- `rlm/` — reinforcement learning from memory?
- `scheduler/` — task scheduling
- `skills/` — composable capability primitives
- `streaming/` — streaming output
- `tools/` — atomic stateless functions
- `validation/` — input/output validation

### Key Primitives
- **Tools → Skills → Agents → DeepAgent** hierarchy (atomic → composable → autonomous → hierarchical)
- **Dynamic DAGs** — runtime workflow composition (not static graphs)
- **Memory scoping + TTL** — prevents context bleed between agents
- **Full provenance tracking** — every context change is attributable
- **Deterministic replay** — record a run, replay it exactly
- **Token budgeting** — hard budget enforcement at the framework level

### Quality Signals
- 1,557 passing tests, 80% coverage
- MyPy typed throughout
- Ruff + pre-commit enforced
- CI on GitHub Actions
- CHANGELOG + CONTRIBUTING + CODE_OF_CONDUCT
- Community Discord: discord.gg/C8ZXAbD8

---

## Relevance to West AI Labs

**High relevance to Nebulus-Gantry** (orchestration layer) and **Nebulus-Core** (shared services).

Specific overlap:
1. **Token budgeting** — exactly the kind of infrastructure Gantry needs to prevent runaway context consumption across concurrent agent tasks
2. **Memory scoping with TTL** — directly addresses context isolation requirements for multi-tenant Nebulus deployments
3. **Deterministic replay** — enormous value for debugging agent failures in production; we'd want this in Nebulus's observability story
4. **Protocol-first design** — aligns with Nebulus's composability goals; you can slot CEMAF's context management into existing agent stacks without replacing them
5. **DAG orchestration with dependency resolution** — Gantry uses DAG-based task scheduling; CEMAF's planner/executor architecture is worth studying

**What CEMAF doesn't solve** (gaps = opportunities):
- No DLP / data exfiltration controls
- No trust boundary enforcement between agents
- No local-first / offline-first design (appears cloud-agnostic but cloud-leaning)
- Security controls are minimal (moderation hook exists but no prompt injection defense)

---

## Recommended Next Steps

1. **Read `src/cemaf/orchestration/deep_agent.py`** — understand how hierarchical context isolation works
2. **Read `src/cemaf/memory/protocols.py`** — steal the memory scoping interface for Nebulus-Core
3. **Study `src/cemaf/replay/`** — deterministic replay design is directly applicable to Gantry
4. **Compare CEMAF's token budgeting to our current approach** — if we don't have one, use CEMAF's
5. **Watch the repo** — 0 stars today but solid engineering; this could grow fast
