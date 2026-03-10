# cognee Scout — 2026-03-07

**Repo:** https://github.com/topoteretes/cognee  
**Fork:** https://github.com/moto-westai/cognee  
**Clone:** /home/jlwestsr/projects/research-temp/cognee (shallow)  
**Stars:** ~13,000 (established project, created 2023-08-16)  
**Language:** Python  
**Updated:** 2026-03-07  

---

## What It Does

Cognee is an open-source "knowledge engine" for AI agent memory. Tagline: "Memory for AI Agents in 6 lines of code." It transforms raw data (documents, past conversations, images, audio) into persistent, queryable agent memory by combining:

- **Vector search** (semantic similarity)
- **Graph databases** (relationship-aware knowledge graphs)
- **Self-improvement pipelines** (data evolves as it's ingested)

Core workflow: `add()` data → `cognify()` (knowledge graph construction) → `search()` (query by semantic/graph/hybrid methods).

**Integrations:** 30+ data sources via Pythonic pipelines. Supports multiple backends — LanceDB, PostgreSQL (pgvector), Weaviate, Qdrant, Falkordb, Neo4j for storage; OpenAI, Anthropic, Ollama, Mistral, Gemini for LLMs.

**Deployment options:** Python library, Docker Compose, MCP server (`cognee-mcp/`), REST API, distributed mode.

**Scale signals:** Product Hunt top post, Trendshift badge, 13K stars, active Discord. This is real adoption.

---

## Architecture Highlights

**Top-level structure:**
- `cognee/` — core library
- `cognee-mcp/` — MCP server wrapper (direct MCP integration!)
- `cognee-frontend/` — web UI
- `cognee-starter-kit/` — quick-start examples
- `deployment/` — Kubernetes, Docker configs
- `distributed/` — multi-node architecture
- `evals/` — evaluation suite

**Key design patterns:**
1. **Modular pipelines:** Custom tasks can be injected into the ingestion/cognification pipeline
2. **Multi-backend storage:** Pluggable vector, graph, and relational backends
3. **MCP-native:** Ships an MCP server in `cognee-mcp/` — agents can call cognee directly via MCP protocol
4. **Knowledge graph construction:** Automatic entity extraction and relationship mapping during ingestion, not just embedding

---

## Relevance to West AI Labs

**High relevance, different threat/opportunity surface than mcp-zero.**

1. **Direct competition check:** Cognee is doing agent memory with knowledge graphs. West AI Labs' approach (via OpenClaw's memory system + RAG) is more persona/context oriented. Cognee is more "enterprise knowledge base for agents." Not direct competition, but adjacent.

2. **MCP integration pattern:** `cognee-mcp/` is a working example of wrapping a knowledge engine as an MCP server. If Nebulus-Core needs a persistent memory layer accessible to agents via MCP, this is the reference implementation to study.

3. **Graph + vector hybrid:** Their approach of combining graph relationships with vector similarity is architecturally interesting. Pure vector RAG (ChromaDB) misses relationship traversal. Cognee's dual approach could inform how Nebulus RAG evolves.

4. **Local-first gap:** Cognee supports Ollama (local LLMs) but the default demo path requires OpenAI. Not truly local-first by design — it's "cloud-first with local fallback." West AI Labs differentiates by being local-first by default.

5. **Scale/maturity:** 13K stars means this is the incumbent in Python agent memory. Any pitch comparing West AI Labs' memory approach needs to account for cognee.

**Recommended next steps:**
- Explore `cognee-mcp/` — understand how they expose memory ops as MCP tools
- Read their knowledge graph construction code — how do they extract entities and relationships at ingestion time?
- Test local-only setup (Ollama + LanceDB) — validate whether "local-first" claim holds up in practice
- Consider: cognee as a component rather than something to build — could Nebulus-Core integrate cognee for agent memory instead of building custom?
