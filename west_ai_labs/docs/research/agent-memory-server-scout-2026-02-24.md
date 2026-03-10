# Research: redis/agent-memory-server
**Scout Date:** 2026-02-24  
**Stars:** 187  
**Fork:** https://github.com/moto-westai/agent-memory-server  
**Upstream:** https://github.com/redis/agent-memory-server  
**Clone:** ~/projects/research-temp/agent-memory-server

---

## What It Does

Official Redis project — a **memory layer for AI agents** built on Redis Stack (vectors + hash + search). Exposes both a REST API and MCP server. Ships a Python SDK. Version 0.13.2.

## Architecture Highlights

### Dual Interface
- **REST API** (FastAPI) — CRUD for memories, session management, search
- **MCP Server** (SSE mode) — MCP-native tool surface, port 9000

### Two-Tier Memory Model
- **Working memory** — session-scoped, ephemeral, fast. Files: `working_memory.py`, `working_memory_index.py`
- **Long-term memory** — persistent, vector-searched, topic/entity-tagged. File: `long_term_memory.py`

### Configurable Memory Strategies (`memory_strategies.py`)
Pluggable extraction via abstract `BaseMemoryStrategy`:
- `DiscreteMemoryStrategy` — episodic + semantic fact extraction
- `SummaryMemoryStrategy` — conversation summarization
- `PreferencesMemoryStrategy` — user preference tracking
- Custom strategies supported

### LLM Integration
- Multi-provider via LiteLLM (OpenAI, Anthropic, Bedrock, Ollama, Azure, Gemini)
- Used for: topic extraction, entity recognition, conversation summarization, memory consolidation

### Security (`prompt_security.py`)
Built-in prompt injection defense — pattern matching against ~15 adversarial patterns:
- Instruction override attempts ("ignore previous instructions")
- Jailbreak patterns ("act as DAN", "pretend you are")
- Information extraction ("reveal your system prompt")
- Code execution attempts

This is notable — they're thinking about security at the memory layer, not just the inference layer.

### Background Tasks
Two modes:
- `asyncio` — single-process dev mode
- `Docket` — production, separate task-worker containers for non-blocking background processing (memory consolidation, summarization)

### Deployment
Full Docker Compose stack — API + task-worker + Redis + MCP containers. Also available on Docker Hub (`redislabs/agent-memory-server`).

## Relevance to West AI Labs

**Very high relevance.** This is basically a reference implementation for what Nebulus-Core's memory subsystem should look like.

1. **Direct template** — The two-tier working/long-term memory split + pluggable extraction strategies is exactly the architecture we'd design for Nebulus. We can follow this pattern without reinventing it.

2. **MCP-native** — Ships an MCP server. Nebulus-Gantry could integrate this directly or wrap it.

3. **Prompt security module** — `prompt_security.py` is a rare example of injection defense at the memory layer. Should extract and adapt this for any Nebulus memory component.

4. **Redis dependency** — We're already Redis-adjacent (it's in our infra consideration). This validates Redis Stack as a solid vector+memory backend.

5. **Pluggable strategies** — The `BaseMemoryStrategy` ABC is clean design we could adopt for our own memory interface spec.

## Gaps / Concerns
- Requires Redis Stack (not just vanilla Redis) — adds infra complexity for local deploys
- LiteLLM dependency means cloud LLM calls for memory extraction — not fully local-first; Ollama backend mitigates this
- Still early (187 stars, v0.13.2) — API may shift; watch for breaking changes

## Recommended Next Steps
1. **Highest priority:** Read `prompt_security.py` fully and extract the injection patterns for our own security layer
2. Run locally with Redis + Ollama backend — validate fully local-first operation
3. Evaluate MCP server surface vs. what Nebulus-Gantry needs
4. Consider contributing: add a local-only mode that skips LLM summarization (pure vector store, no API calls) — good PR + visibility
