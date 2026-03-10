# Research Note: jnaapakam
**Scout Date:** 2026-03-08  
**Source:** https://github.com/yablokolabs/jnaapakam  
**Fork:** https://github.com/moto-westai/jnaapakam  
**Clone:** /home/jlwestsr/projects/research-temp/jnaapakam  
**Stars:** 0 (fresh, published yesterday)  
**Language:** Python  

---

## What It Is

jñāpakaṁ (Sanskrit: "memory, reminder") is an open protocol for AI agent memory persistence. It formalizes a pattern we already use — SOUL.md, IDENTITY.md, MEMORY.md — and adds a lightweight HTTP memory server on top.

Two-part system:
1. **Soul Schema** — Standard markdown files (SOUL.md, IDENTITY.md, MEMORY.md, USER.md) that define agent identity
2. **Memory API** — HTTP server (SQLite backend) for ingest, query, consolidate, backup/restore

---

## Architecture

```
Agent → jñāpakaṁ Server (port 8889)
              ↓
         Ingest (LLM extracts summary, entities, importance)
              ↓
         SQLite memory.db
              ↓
         Consolidate every 30 min (LLM finds cross-cutting patterns)
              ↓
         Query (natural language → synthesized answer with citations)
```

Key design choice: **LLM-active memory** not passive RAG. Every ingest and consolidation is an LLM pass that extracts structure and finds connections. Tradeoff: more LLM calls, richer cross-referencing. Defends this as appropriate for hundreds-to-low-thousands of memories (our scale).

**No vector database** — SQLite only. Simpler, local-first, sufficient for agent memory workloads.

---

## Soul Schema Files

The protocol standardizes exactly what we already have:
- `SOUL.md` — personality, tone, behavioral boundaries
- `IDENTITY.md` — name, emoji, description
- `MEMORY.md` — curated long-term memory
- `USER.md` — (implied by examples) who the agent serves

This is validation that our file structure is the emerging standard. They even include an OpenClaw integration example in the README.

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | Memory counts |
| `/memories` | GET | List stored memories |
| `/ingest` | POST | Add text `{"text": "...", "source": "..."}` |
| `/query?q=...` | GET | NL query against memory |
| `/consolidate` | POST | Trigger manual consolidation |
| `/backup` | GET | Export all as JSON |
| `/restore` | POST | Import from backup JSON |

Multi-agent support: multiple agents can share one server for collective knowledge.

---

## Relevance to West AI Labs

**High relevance.** This is validation and reference architecture for:

1. **Nebulus-Core** — The memory API design (ingest/consolidate/query) is a clean pattern to study for our own agent memory service. Their "LLM-active consolidation" approach is worth benchmarking against our current passive MEMORY.md approach.

2. **Conductor** — Cross-agent shared memory via a single server is the pattern Conductor needs for multi-agent context sharing. The namespace isolation missing from this project (on the roadmap) is exactly what we'd need to add for DLP.

3. **OpenClaw integration** — They explicitly integrate with OpenClaw. Could run this alongside Moto as a supplemental structured memory layer.

---

## Gaps / Opportunities

- No DLP / namespace isolation (their roadmap item). This is a gap we could fill.
- No encryption at rest (roadmap).
- No memory expiry/retention policies (roadmap).
- Consolidation cost: every 30 min with LLM calls could be expensive at scale. 
- Single-user design — no auth on the API.

Our positioning: enterprise-grade version with DLP, multi-tenant, auth, and local inference.

---

## Recommended Next Steps

1. **Pilot it** — Run alongside Moto, point it at our workspace. See if LLM-active consolidation adds value vs. our manual MEMORY.md curation.
2. **Read the source** — The consolidation algorithm is the interesting part. Could borrow the pattern for Nebulus-Core.
3. **Watch** — Early stage, 0 stars. Could contribute the DLP/namespace work and position West AI Labs as a contributor.
