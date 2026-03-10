# TrippleEffect — Scout Research Note
**Date:** 2026-03-09
**Source:** https://github.com/gaborkukucska/TrippleEffect
**Fork:** https://github.com/moto-westai/TrippleEffect
**Clone:** /home/jlwestsr/projects/research-temp/TrippleEffect
**Stars:** 3 | **Language:** Python | **Updated:** 2026-03-09

---

## What It Does

TrippleEffect is an asynchronous, collaborative multi-agent framework built on Python, FastAPI, and WebSockets. It's at v2.42, actively developed "by various LLMs guided by Gabby" — essentially a self-describing LLM-dev project.

**Architecture:**
- **Admin AI** — central stateful agent (state machine: `conversation` → `planning` → back). Interfaces with user, monitors ongoing projects, routes to PMs.
- **Project Manager (PM) Agent** — auto-spawned per project. Uses Taskwarrior (`tasklib`) to decompose plans, create teams, assign sub-tasks to dynamically-spawned worker agents.
- **Constitutional Guardian (CG) Agent** — specialized agent that reviews final outputs against `governance.yaml` principles. Pauses output on concern, notifies UI. This is a trust/governance layer baked into the framework.
- **Dynamic Worker Agents** — spawned on-demand by PM, assigned specific tasks.

**Tools available to agents:**
- `file_system.py` — filesystem R/W
- `web_search.py` — web search
- `github_tool.py` — GitHub integration
- `project_management.py` — Taskwarrior task CRUD
- `manage_team.py` — spawn/manage worker agents
- `send_message.py` — agent-to-agent messaging
- `knowledge_base.py` — internal KB queries
- `command_executor.py` — shell execution

**LLM Providers:**
- Ollama (local, default `http://localhost:11434`)
- OpenAI
- OpenRouter
- Provider-level retry with backoff, failover handler present

**UI:** WebSocket-based, served via FastAPI at `localhost:8000`

---

## Architecture Highlights

- Full async/await throughout (aiohttp, FastAPI)
- State machine per agent (`agent_lifecycle.py`, `state_manager.py`)
- Performance tracker per agent
- Workflow manager + cycle_handler for agent reasoning loops
- Provider key manager (rotates API keys)
- Session manager for multi-session support
- The `helperfiles/DEVELOPMENT_RULES.md` is a meta-file instructing LLMs how to develop the framework — self-modifying system

---

## Relevance to West AI Labs

**High relevance.** Several architectural patterns are worth studying:

1. **Constitutional Guardian** — closest thing to a built-in DLP/governance layer in an open-source multi-agent system. West AI Labs' security-first positioning could learn from or improve on this pattern. CG as a first-class agent (not middleware) is an interesting design choice.

2. **Admin AI + PM hierarchy** — mirrors the orchestrator→sub-agent pattern we're building in Nebulus-Gantry. The state machine approach for the top-level agent is clean.

3. **Taskwarrior as task backend** — clever use of an existing tool for task persistence. Nebulus-Gantry should consider pluggable task backends rather than building from scratch.

4. **Provider failover + key rotation** — production-grade concern handled here. Relevant for Nebulus-Core shared services.

**Gaps in TrippleEffect vs. West AI Labs positioning:**
- No context isolation between agents — agents can message freely
- Constitutional Guardian is output-only review, not input filtering (prompt injection blind spot)
- Cloud-dependent for powerful models (no local-first default)
- No trust scoring or DLP at the communication layer

---

## Recommended Next Steps

- Study `constitutional_guardian` implementation for governance patterns
- Study `agent_lifecycle.py` state machine for Nebulus-Gantry agent lifecycle design
- Note the `DEVELOPMENT_RULES.md` pattern — worth considering for Nebulus agent dev guidelines
- Flag: This project is actively LLM-developed; code quality may be inconsistent
