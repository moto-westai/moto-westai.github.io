# ctxvault — Scout Research
**Repo:** Filippo-Venturini/ctxvault  
**Fork:** moto-westai/ctxvault  
**Stars:** 10 | **Updated:** 2026-02-27 | **Language:** Python  
**PyPI:** `pip install ctxvault`

## What It Does
Local semantic memory infrastructure for AI agents. Agents get persistent, queryable knowledge through isolated **vaults** — one per agent, per project, or shared. No cloud, no telemetry.

## Architecture
- **Storage:** ChromaDB (PersistentClient, telemetry disabled) — one collection per vault
- **Integration modes:**
  - **CLI:** `ctxvault init/add/query` — manual inspection and control
  - **HTTP API:** FastAPI app — programmatic integration (LangChain, LangGraph, custom pipelines)
  - **MCP server:** Agents self-manage memory via MCP protocol (no code required)
- **Document model:** Pydantic `DocumentInfo` with doc_id, source, chunk count, filetype
- **Text processing:** Chunking util, metadata builder, multi-format extraction
- **Config:** Per-vault config dict with `db_path`

## Key Design Choices
- Multi-vault isolation — each vault has its own Chroma collection + history
- MCP-first for agent autonomy + CLI for human observability (good separation)
- No external deps beyond ChromaDB + FastAPI — very clean
- Telemetry explicitly disabled (`anonymized_telemetry=False`)

## Relevance to West AI Labs
**HIGH.** This maps almost directly onto what Nebulus-Core needs for a memory layer:
- Local-first, no cloud — aligns perfectly with West AI Labs ethos
- MCP integration means it could slot into Nebulus-Gantry agent workflows immediately
- Isolated vaults = clean isolation primitive for per-agent context
- Observable (CLI) + autonomous (MCP) — same dual-mode philosophy we want

## Recommended Next Steps
1. Test locally: `pip install ctxvault` and run MCP server against Claude Desktop
2. Evaluate as the memory backend for Nebulus-Core agent context
3. Consider contributing: add vault-level access controls / encryption at rest
4. Watch for growth — 10 stars but fresh, could become reference implementation
