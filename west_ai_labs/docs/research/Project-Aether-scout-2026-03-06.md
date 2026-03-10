# Project Aether — Research Note
**Date:** 2026-03-06
**Repo:** Gamingstein/Project-Aether → fork: moto-westai/Project-Aether
**Clone:** /home/jlwestsr/projects/research-temp/Project-Aether
**Stars:** 1 (fresh, active dev)
**Language:** Python 3.12+
**License:** MIT

---

## What It Does

A production-grade, event-driven AI Discord bot built as a **microservices system modeled after a biological organism**. Each service is an "organ": a Gateway (sensory input), a Brain (LangGraph reasoning), a Cerebellum (response timing/typing simulation), an MCP Server (tool discovery), and a ChromaDB memory store. Services communicate via Redis Streams. Fully observable with Prometheus + Grafana (20-panel dashboard).

This is a **portfolio showcase** but with **genuine production engineering** — not a toy.

---

## Architecture Highlights

### Services
```
Gateway (Discord)  ──Redis Streams──►  Brain (LangGraph StateGraph)
                                            │
                                            ├── MCP Server (tool auto-discovery, FastMCP + FastAPI, :8080)
                                            ├── ChromaDB (async vector memory, tiktoken RAG)
                                            └── Amygdala (mood/sentiment engine)

Cerebellum (typing simulation) ◄── Brain (reply_intent stream)

Dashboard (FastAPI + WebSocket, :8000) ── observes everything
Prometheus (:9099) + Grafana (:3000) — 20 panels
PostgreSQL 16 (Alembic migrations)
```

### The Brain (most interesting service)
- **LangGraph StateGraph** with 8 discrete nodes, tool-calling loop, intent-based routing
- **Prompt injection protection** — 10 pattern families, sanitization before any LLM call
- **MCP auto-discovery** — zero Brain changes to add new tools; just deploy a new MCP endpoint
- **Async ChromaDB RAG** with tiktoken token windowing (default: 2,000 token budget for context retrieval)
- **Amygdala** — mood tracking via LLM sentiment classification (float score -1.0 to 1.0), keyword fallback

### Security
- Rate limiting: sliding-window per user (Redis sorted sets), fail-open, configurable max messages/window
- Prompt injection: 10 pattern families, sanitizes before LLM call
- MCP: bearer token auth on all tool endpoints
- Trace IDs propagated across all services for correlation

### Quality Signals
- 735 passing tests (unit + integration)
- Ruff lint + format enforced
- Alembic database migrations
- Docker Compose for full stack
- GitHub Actions CI
- SECURITY.md (threat model documented)
- structlog JSON logging with trace-ID correlation

---

## Relevance to West AI Labs

**High relevance to OpenClaw-adjacent work** and **Nebulus observability story**.

Specific overlap:
1. **Prompt injection protection (10 pattern families)** — directly applicable to Nebulus-Core's security layer; this is production-tested code worth studying. The 10 families are worth cataloging for our DLP work.
2. **MCP auto-discovery pattern** — zero-config tool registration is exactly what Conductor needs; agents should discover capabilities dynamically, not have them hardcoded
3. **Redis Streams for async inter-service messaging** — Nebulus-Gantry needs an async event bus; Redis Streams is a solid, simple choice vs. Kafka
4. **Token windowing for RAG** — tiktoken-based budget enforcement for vector retrieval; directly applicable to Nebulus memory management
5. **Mood/sentiment tracking via Amygdala** — interesting for OpenClaw agent state awareness; an agent that tracks conversation tone could adapt behavior
6. **Observability** — the Prometheus + Grafana pattern with 20 panels is a reference implementation for Nebulus observability layer

**What this proves:** The MCP + LangGraph + ChromaDB stack is production-viable. The architecture validates the approach Jason is taking with Nebulus.

**What it doesn't do:**
- No local inference (all cloud LLM)
- No DLP/data sovereignty
- Not designed for multi-tenant or enterprise
- The Discord surface is specific; the Brain/MCP/Redis pattern is the transferable part

---

## Recommended Next Steps

1. **Read `services/brain/graph.py`** — the LangGraph StateGraph topology; understand the 8 nodes and routing
2. **Extract the prompt injection patterns** from `services/brain/` — catalog the 10 families for Nebulus-Core security baseline
3. **Study `services/brain/mcp_client.py`** — how auto-discovery works over Streamable HTTP; use for Conductor
4. **Review `services/brain/amygdala.py`** — the sentiment engine is clean, standalone, worth porting
5. **Steal the Prometheus metrics pattern** — the 20-panel Grafana config is reusable for Nebulus observability
