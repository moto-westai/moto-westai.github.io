# OpenCortex — Scout Note
**Date:** 2026-02-26  
**Source:** https://github.com/StardustVision/OpenCortex  
**Fork:** https://github.com/moto-westai/OpenCortex  
**Stars:** (new, Chinese-language project)  
**Last Updated:** 2026-02-27

## What It Does
AI agent memory and context management system, ported/refactored from OpenViking (Volcengine). Provides multi-tenant memory with SONA reinforcement learning-based ranking. MCP server exposes 6 tools. Integrates with Claude Code via hooks and plugin system.

## Architecture Highlights

### Three-Layer Summaries (L0/L1/L2)
- Return precision tiers on demand — saves tokens by returning only as much detail as needed

### SONA Self-Learning Ranking
- Reinforcement learning-driven — high-value memories surface, low-value memories decay naturally
- Not a static similarity score, adapts over time based on what the agent finds useful

### Multi-Tenant Isolation
- URI namespace isolation per tenant/user — multiple teams/agents share infra without data leakage
- `tenant_id` + `user_id` in config

### MCP Server (FastMCP v3)
- Exposes 6 memory tools to external agents
- Both stdio (Claude Code/Desktop) and SSE (remote agents) transport modes
- Hooks: session-start, session-end, user-prompt-submit, stop — automatic memory capture

### Embedding Provider
- Volcengine `doubao-embedding-vision-250615` — China cloud dependency (downside)
- Pluggable enough to swap out

### Vector Backend
- Custom `ruvector-server.js` — not Qdrant/Chroma, proprietary JS vector store

## Relevance to West AI Labs
**MEDIUM.** The SONA reinforcement ranking concept is interesting and differentiating. The multi-tenant isolation pattern is directly relevant to Nebulus-Gantry multi-org deployments. However:
- **Volcengine dependency** is a blocker for production West AI use — needs local embedding swap
- **Chinese-language README/comments** — adds friction for team adoption
- **Custom JS vector store** rather than standard (Qdrant/Chroma) — less portable
- Plugin/hooks architecture mirrors what Meridian does but less polished

## Recommended Next Steps
1. **Extract the SONA ranking concept** — RL-based memory importance decay is novel, worth prototyping in Python
2. **Skip direct adoption** — Volcengine cloud dependency + non-standard vector store = too much rework
3. **Keep watching** — if they swap to a local embedding model it becomes more viable
