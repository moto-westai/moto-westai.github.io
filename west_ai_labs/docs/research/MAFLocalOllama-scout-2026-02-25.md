# Research Note: MAFLocalOllama
**Scouted:** 2026-02-25  
**Source:** https://github.com/frdeange/MAFLocalOllama  
**Fork:** https://github.com/moto-westai/MAFLocalOllama  
**Clone:** `/home/jlwestsr/projects/research-temp/MAFLocalOllama`  
**Stars:** 0 (fresh — 2026-02-25)  
**Language:** Python (FastAPI backend) + TypeScript (Next.js frontend)

---

## What It Does

Full-stack multi-agent travel planner using **Microsoft Agent Framework (MAF)** with **Ollama** for 100% local LLM inference. Three specialized agents (Researcher → WeatherAnalyst → Planner) collaborate in a sequential pipeline, streaming results to a React/Next.js UI via SSE.

No OpenAI or cloud LLM APIs — all inference runs locally through Ollama (default: `phi4-mini`).

---

## Architecture Highlights

### Agent Pipeline
```
User (Browser) → Next.js → FastAPI
                              ↓
            Researcher → WeatherAnalyst → Planner
                              ↓
                       MCP Tool Server (FastMCP)
```

- Uses `SequentialBuilder` from MAF for pipeline construction
- Agents: role-specific system prompts, stateless except for shared conversation history
- WeatherAnalyst is MCP-tool-enabled (weather, time, restaurant lookups)

### Stack
| Component | Tech |
|---|---|
| LLM Inference | Ollama (local, GPU/CPU) |
| Agent Framework | Microsoft Agent Framework (MAF) |
| Backend API | FastAPI + SSE streaming |
| Frontend | Next.js / React |
| MCP Integration | FastMCP (Streamable HTTP) |
| Persistence | PostgreSQL (conversation history, context windowing) |
| Observability | OpenTelemetry → Aspire Dashboard (traces + metrics + logs) |
| Orchestration | Docker Compose (GPU + CPU profiles) |
| Testing | pytest (190 tests), architecture compliance tests |

### Key Code Patterns
- `src/config.py` — frozen dataclass for settings from env vars (clean, production-grade)
- `src/workflows/travel_planner.py` — `SequentialBuilder` wiring, MCP tool as context manager
- `src/telemetry.py` — OpenTelemetry setup
- `mcp_server/` — FastMCP tool definitions for weather/time/restaurants
- `AGENTS.md` — MAF agent instructions file (interesting pattern — like our AGENTS.md)

---

## Relevance to West AI Labs / Nebulus

**High relevance.** This is essentially a reference implementation of what Nebulus-Gantry should be doing:

1. **Local-first LLM inference via Ollama** — matches Nebulus-Atom / Nebulus-Edge goals
2. **MCP integration** — FastMCP as a tool server in Docker; Nebulus is building MCP-first
3. **SSE streaming** — real-time agent output streaming pattern we'll need in Nebulus UX
4. **OpenTelemetry observability** — traces + metrics pattern worth adopting in Nebulus-Core
5. **Docker Compose GPU/CPU profiles** — same dual-profile strategy Nebulus uses
6. **190 architecture compliance tests** — impressive test discipline for this scale

### Gaps / Limitations
- Domain is travel planning (trivial use case, but architecture is the point)
- No memory/state persistence across sessions
- MAF is Microsoft's framework — may have vendor lock-in considerations vs. our own orchestration
- No security/auth layer on API

---

## Recommended Next Steps

1. **Study the MCP server pattern** — FastMCP Streamable HTTP setup is clean; adapt for Nebulus MCP tool host
2. **SSE streaming pattern** — borrow the FastAPI SSE implementation for Nebulus API layer
3. **OpenTelemetry setup** — copy the OTEL + Aspire dashboard pattern into Nebulus-Core observability
4. **Architecture tests** — the "compliance tests" idea (pytest checking import boundaries) is worth adopting in Nebulus

---

## Notes
- Uses Microsoft's `agent_framework` pip package (not open-sourced, installed via requirements)
- `AGENTS.md` in the repo is literally instructions for AI coding assistants — same pattern as our workspace
- Very clean, well-documented Python. Production-grade code quality for a PoC.
