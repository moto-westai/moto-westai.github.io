# meridian — Scout Note
**Date:** 2026-02-26  
**Source:** https://github.com/GigaClaude/meridian  
**Fork:** https://github.com/moto-westai/meridian  
**Stars:** (new repo, minimal)  
**Last Updated:** 2026-02-27

## What It Does
Persistent memory system for Claude Code, running entirely on local GPU. Solves context compaction memory loss by maintaining a three-tier storage system with a local LLM synthesis layer.

## Architecture Highlights

### Three-Tier Storage
- **Hot:** YAML briefing (~1,500 tokens) at session start — current task, recent decisions, active warnings
- **Warm:** Qdrant vector store with importance-weighted reranking + freshness decay — searched on demand
- **Cold:** Gzipped session transcripts indexed by date — keyword-searchable archive

### Synthesis Gateway
- Local LLM via Ollama (`llama3.2` or similar) synthesizes top-10 Qdrant results into ~500 tokens
- Volatile content detection (ports, PIDs, /tmp paths) filtered before storage
- Structured JSON schema forces briefing into typed fields (decisions, warnings, next_steps, etc.)

### MCP Server + Plugin Architecture
- Ships as an MCP server (`mcp_server.py`)
- Also includes Claude Code plugin (`plugin/`) with hooks (`prerecall.py`) and skills (`remember`, `recall`, `briefing`)
- **Prerecall hook** fires every prompt, auto-injects top-3 relevant memories — 51ms P50 latency
- Multi-agent: memories carry `source` tag — multiple Claude instances share one Meridian backend

### Storage Stack
- `Qdrant` (vector similarity) + `SQLite` (relational — decisions, entities, relations) + JSON on disk (episodic sessions)
- Memory types: `MemoryRecord`, `Decision`, `Entity`, `Relation`, `Warning`, `Checkpoint`
- `_VOLATILE_PATTERNS` regex — filters ephemeral data before it pollutes memory

## Relevance to West AI Labs
**HIGH.** This is essentially what Moto's own memory system should be — but productized for Claude Code. Key intersections:
- Nebulus-Core memory service concept validated — Meridian proves the architecture (hot/warm/cold tiers, local LLM synthesis)
- The volatile-content filtering pattern is worth copying verbatim
- MCP server delivery model matches Nebulus-Gantry's integration pattern
- Multi-agent sourcing (`source` tag) directly applicable to Nebulus multi-agent workflows

## Recommended Next Steps
1. **Steal the volatile content filter** — `_VOLATILE_PATTERNS` regex list is solid, adopt in Nebulus-Core memory
2. **Study the briefing schema** — the JSON schema-forced structured output is clever (Ollama `format` param)
3. **Consider integrating** Meridian as Moto's own memory backend — it already works with Claude Code's plugin system
4. **Watch for star growth** — if this takes off it'll be a major reference implementation
