# Research: jundot/omlx
**Scout Date:** 2026-02-24  
**Stars:** 70  
**Fork:** https://github.com/moto-westai/omlx  
**Upstream:** https://github.com/jundot/omlx  
**Clone:** ~/projects/research-temp/omlx

---

## What It Does

**oMLX** — LLM inference server for Apple Silicon, built on mlx-lm with continuous batching, paged SSD KV cache tiering, multi-model serving, and a macOS menu bar app. Python 3.10+, Apple Silicon only (M1/M2/M3/M4).

The creator's origin story is worth noting: *"Every LLM server I tried made me choose between convenience and control... oMLX persists KV cache to SSD - even when context changes mid-conversation, all past context stays cached and reusable across requests... That's why I built it."* — This is exactly the friction Nebulus-Edge needs to solve.

## Architecture Highlights

### Core Engine (`engine_core.py`, `scheduler.py`)
- `EngineCore` — continuous batching loop, vLLM-inspired design adapted for MLX
- `Scheduler` + `SchedulerConfig` — manages prefill/decode batching, configurable batch sizes
- Adapts `vllm-mlx` (waybarrios fork) as the base inference engine

### Paged KV Cache with SSD Tiering
- Block-based cache management (prefix sharing + Copy-on-Write, inspired by vLLM)
- When GPU (unified) memory fills up → blocks offload to SSD
- On next request with matching prefix → restored from disk, not recomputed
- **Survives server restarts** — cache persists across process boundaries
- Directly solves the "cold start" problem for local agent workflows with long contexts

### Multi-Model Serving (`engine_pool.py`, `model_registry.py`)
- Load LLMs + embedding models + rerankers in same server
- LRU eviction when memory runs low
- Pinning for frequently-used models
- Model discovery from directory (no manual config)

### MCP Integration (`omlx/mcp/`)
- `tools.py`, `manager.py`, `executor.py`, `config.py` — full MCP server
- `mcp.example.json` — config example

### Admin Dashboard + Model Downloader
- Web UI at `/admin` — model management, chat, real-time monitoring, per-model settings
- HuggingFace model search + download built in
- Menu bar app (DMG) — no terminal required for casual use

### API Compatibility
- `POST /v1/chat/completions` — OpenAI
- `POST /v1/messages` — Anthropic native API
- `POST /v1/embeddings`, `POST /v1/rerank`
- Drop-in replacement for both OpenAI and Anthropic SDKs

### Claude Code Optimization (notable)
- Scales reported token counts so Claude Code's auto-compact triggers at right timing
- SSE keep-alive prevents read timeouts during long prefill
- Direct design acknowledgment that Claude Code is a primary target workload

## Relevance to West AI Labs

**Extremely high relevance for Nebulus-Edge.** This is one of the most directly applicable repos we've scouted.

1. **Nebulus-Edge reference implementation** — oMLX solves the exact Apple Silicon inference server problem Nebulus-Edge targets. The SSD KV cache alone is a major feature gap in all other MLX servers.

2. **Architecture to study, not fork wholesale** — The vLLM-inspired engine design (EngineCore → Scheduler → EnginePool) is cleaner than rolling our own. We should evaluate adopting this pattern for Nebulus-Edge's inference layer.

3. **MCP server built-in** — Already has MCP integration. Nebulus-Gantry could connect to oMLX as a backend tool provider.

4. **Embedding + reranking co-located** — Serving embeddings + rerankers in the same process as LLMs is exactly what Nebulus-Edge needs for offline RAG workflows.

5. **Claude Code optimization** — Shows that serious local ML devs are targeting Claude Code as the agent UX. Our tooling should match.

## Gaps / Concerns
- macOS-only (Apple Silicon) — fine for Nebulus-Edge, not applicable to Nebulus-Prime (Linux/NVIDIA)
- Small project (70 stars) — one developer, no org backing, bus factor = 1
- Pulls mlx-lm from a specific commit hash — maintenance burden if upstream diverges
- No auth/multi-tenant story visible — single-user local deployment assumed

## Recommended Next Steps
1. **Highest priority:** Test on nebulus (Mac Mini M4 Pro) — validate SSD KV cache performance with long-context workloads
2. Study `engine_core.py` + `scheduler.py` — extract the batching design for Nebulus-Edge
3. Audit `omlx/mcp/` — compare MCP tool surface to what we need; may be directly usable
4. Open a conversation with the author (jundot) — this person is building in our space; potential collaborator or contributor to Nebulus-Edge
5. Track upstream commits — this is moving fast (updated 2026-02-25)
