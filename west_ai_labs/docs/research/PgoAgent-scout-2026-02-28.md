# PgoAgent — Scout Research
**Repo:** Soul-XuYang/PgoAgent  
**Fork:** moto-westai/PgoAgent  
**Stars:** 6 | **Updated:** 2026-02-05 | **Language:** Python + Go  
**Version:** v0.0.3

## What It Does
Full-stack multi-agent system: LangGraph Python agents + Go gRPC/Gin web backend. Combines long+short-term memory, Agentic RAG (dual-threshold + BM25 + vector + rerank), MCP tool integration, local LLM deployment via vLLM, and model fine-tuning pipeline.

## Architecture
```
User (Web/CLI)
  → Go Gin HTTP API (Swagger-documented)
  → gRPC bridge (streaming, incremental LLM output)
  → Python LangGraph agent core
    ├── decisionAgent.py  — tool call routing
    ├── planAgent.py      — task decomposition
    └── memoryAgent.py    — long-term memory management
  → RAG Engine (ChromaDB + BM25, dual threshold, rerank)
  → vLLM local deployment (chat + embedding + rerank models)
  → PostgreSQL (user data, conversation history, long-term memory)
```

### Notable Subsystems
- **Agentic RAG:** Dual-threshold hybrid retrieval (vector + BM25) with rerank pass; iterative loop with depth limit
- **Memory:** PostgreSQL for structured long-term memory (configurable retention), ChromaDB for vector recall
- **MCP:** External MCP server integration (`mcp_external_server.py`) — pluggable tool ecosystem
- **Fine-tuning module:** Full pipeline: dataset split → clean → convert → train → merge → deploy via vLLM
- **gRPC streaming:** Python↔Go communication, supports streaming LLM output

## Key Design Choices
- Python/Go split: agent logic in Python, web/API in Go (performance boundary is smart)
- gRPC for cross-language bridge with streaming support — production-grade choice
- PostgreSQL over SQLite for memory — scales to multi-user / multi-session workloads
- Integrated fine-tuning pipeline is rare and valuable for local model customization

## Relevance to West AI Labs
**MEDIUM.** More of a reference architecture than a direct adoption candidate:
- Python/Go split with gRPC streaming is a pattern worth studying for Nebulus service boundaries
- Agentic RAG with dual-threshold + rerank is more sophisticated than most repos — review `RagEngine.py`
- Local vLLM deployment + fine-tuning pipeline directly relevant to Nebulus-Prime
- Chinese codebase/docs — some friction, but architecture is clean and English README exists

## Recommended Next Steps
1. Read `src/agent/rag/RagEngine.py` — dual-threshold hybrid retrieval is worth understanding
2. Study gRPC bridge pattern for potential Nebulus-Gantry↔service communication
3. Low stars but solid engineering — monitor for updates
