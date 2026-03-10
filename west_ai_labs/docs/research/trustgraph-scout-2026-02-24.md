# Research: trustgraph-ai/trustgraph
**Scout Date:** 2026-02-24  
**Stars:** 1,312  
**Fork:** https://github.com/moto-westai/trustgraph  
**Upstream:** https://github.com/trustgraph-ai/trustgraph  
**Clone:** ~/projects/research-temp/trustgraph

---

## What It Does

TrustGraph is a **context backend for AI agents** — a unified system providing durable, portable "context cores" that agents can query across sessions and deployments. Positioned as the memory+knowledge layer sitting under any LLM/agent system.

Key value prop: "reduce hallucinations with grounded context retrieval" — retrieves from structured knowledge graphs rather than raw vector similarity alone.

## Architecture Highlights

### Multi-Model Database Stack
- **Relational/K-V** — tabular structured data
- **Document store** — text corpora
- **Graph DB** — RDF triples via ontology/SPARQL (schema.ttl present)
- **Vector store** — semantic similarity search
- **Multimodal** — images, video, audio ingestion (planned/partial)

### Packaging Structure (monorepo, 740 Python files)
- `trustgraph/` — core library
- `trustgraph-base/` — base services
- `trustgraph-cli/` — rich CLI (~30+ commands: load-text, invoke-rag, show-flows, etc.)
- `trustgraph-flow/` — workflow composition engine
- `trustgraph-mcp/` — MCP server integration (tools.py, manager.py, executor.py)
- `trustgraph-embeddings-hf/` — HuggingFace embedding pipelines
- `trustgraph-bedrock/`, `trustgraph-vertexai/` — cloud LLM connectors
- `trustgraph-ocr/` — document OCR ingestion

### Deployment
- Docker Compose or Kubernetes via `npx @trustgraph/config` (generates deploy.zip)
- All containers, no bare-metal assumption
- Workbench UI on port 8888 (chat, graph viz, knowledge management)

### LLM Backend Support
- API: Anthropic, OpenAI, Cohere, Gemini, Mistral
- Self-hosted: vLLM, Ollama, TGI, LM Studio, Llamafiles

### Context Cores (key differentiator)
Packaged, versioned knowledge bundles you can move between projects/environments — like Docker images but for grounded context.

## Relevance to West AI Labs

**High relevance.** Several angles:

1. **Nebulus-Core memory layer** — TrustGraph's graph+vector hybrid is exactly what Nebulus-Core needs for agent context persistence. Worth evaluating as an upstream dependency vs. rolling our own.

2. **MCP integration** (`trustgraph-mcp/`) — already has tools.py + executor pattern. Directly maps to how Nebulus-Gantry would expose context to MCP-enabled agents.

3. **Context Cores concept** — their portable knowledge bundle idea aligns well with Nebulus-Atom runtime atoms. Could influence Nebulus packaging spec.

4. **Ontology-first retrieval** — graph-structured retrieval beats pure RAG for precision. Relevant to our ChromaDB + NetworkX stack.

## Gaps / Concerns
- Heavy stack — full deploy is many containers (Cassandra? Pulsar? TBD). May be overkill for edge.
- Cloud-first deploy tooling (Kubernetes config builder) — Nebulus is local-first, so we'd lean Docker Compose path only.
- 740 Python files is a large codebase to audit; depth of MCP integration not fully verified.

## Recommended Next Steps
1. Test the Docker Compose quickstart locally — see if it runs on shurtugal-lnx
2. Audit `trustgraph-mcp/` in detail — evaluate MCP tool surface as a model for Nebulus-Gantry's MCP server
3. Read `specs/` and `ontology-prompt.md` — understand their knowledge structuring approach
4. Evaluate Context Cores spec as inspiration for Nebulus-Atom packaging format
