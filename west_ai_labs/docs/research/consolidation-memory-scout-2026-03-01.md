# Research: consolidation-memory (charliee1w/consolidation-memory) — 2026-03-01

**Stars:** 5 | **Language:** Python | **Updated:** 2026-03-01
**Fork:** https://github.com/moto-westai/consolidation-memory
**Clone:** /home/jlwestsr/projects/research-temp/consolidation-memory
**PyPI:** `pip install consolidation-memory`

## What It Does

Local-first persistent memory for AI agents. Stores episodes (conversations, facts, solutions) in **SQLite + FAISS**, then runs a background consolidation thread every 6 hours that:
1. Clusters similar episodes by semantic similarity
2. Uses a local LLM to synthesize clusters into structured **knowledge records** (facts, solutions, preferences, procedures)
3. Prunes old episodes, keeping synthesized knowledge

The result: agent memory that compounds and improves over time rather than degrading or filling up.

## Architecture Highlights

- **FastEmbed** for local embeddings — no API keys, runs on laptop
- **SQLite** for episode storage + knowledge records
- **FAISS** for vector similarity search
- **Background consolidation thread** — hierarchical clustering → LLM synthesis
- **MCP server** — drop-in for Claude Desktop/Code/Cursor (15 tools)
- **REST API** — `consolidation-memory serve --rest --port 8080`
- **OpenAI function calling schema** — compatible with any OpenAI-compatible API (Ollama, LM Studio, etc.)

**Key MCP tools:** `memory_store`, `memory_recall`, `memory_search`, `memory_consolidate`, `memory_decay_report`, `memory_protect`, `memory_timeline`, `memory_browse`, `memory_correct`

**Core modules:**
```
src/consolidation_memory/
  client.py          # Main MemoryClient API
  server.py          # MCP server
  database.py        # SQLite schema + ops
  vector_store.py    # FAISS wrapper
  consolidation/     # Clustering + LLM synthesis logic
  backends/          # LLM backend adapters
  schemas.py         # OpenAI function calling schemas
  rest.py            # REST API
  cli.py             # CLI entry point
```

## Why It's Interesting

1. **Hierarchical consolidation** — the cluster-then-synthesize pattern is novel; most memory systems just store and retrieve, this one actively improves its own knowledge base
2. **Fully local** — FastEmbed + local LLM, no cloud dependency. Perfect alignment with West AI Labs local-first values
3. **Memory decay reporting** — tracks which memories are becoming stale, gives agents a way to know what they're forgetting
4. **MCP-native** — immediate integration path with Claude Code / Nebulus tools
5. **`setup-claude` command** — auto-patches `~/.claude/CLAUDE.md` to teach Claude Code to use memory tools proactively. Smart UX.

## Relevance to West AI Labs

- **High** — This is directly applicable to Moto's own persistent memory architecture and to Nebulus-Stack's agent memory layer.
- The consolidation pattern (clustering → synthesis → pruning) should inform how we design long-term agent memory in Nebulus-Atoms.
- Consider evaluating as Moto's memory backend (currently using memory_store/memory_recall via OpenClaw's built-in system — this is more sophisticated).
- The `memory_decay_report` and `memory_protect` tools are features we should consider adding to our memory abstraction.

## Recommended Next Steps

1. Install and test: `pip install consolidation-memory[fastembed] && consolidation-memory init`
2. Run `consolidation-memory setup-claude` and evaluate the CLAUDE.md integration
3. Load test with 268K+ episodes (their benchmark claim) against our typical agent session volumes
4. Consider proposing this as the memory backend for Nebulus-Atoms persistent agent state
