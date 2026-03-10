# Research Note: beezle-bug
**Scouted:** 2026-03-03
**Repo:** https://github.com/rhohndorf/beezle-bug
**Fork:** https://github.com/moto-westai/beezle-bug
**Clone:** /home/jlwestsr/projects/research-temp/beezle-bug
**Stars:** 14 | **Created:** 2024-03-03 | **Last Updated:** 2026-03-03

---

## What It Does

Beezle Bug is a local-first, visual multi-agent orchestration system with a node-based drag-and-drop graph editor (React frontend) and a Python/Flask backend. You wire together agents, knowledge graphs, memory streams, toolboxes, schedulers, and I/O nodes visually, then deploy and chat with the system — locally or against remote LLMs via LiteLLM.

Key features:
- Visual node graph editor for multi-agent pipelines
- Knowledge Graph nodes (entity-relationship, SQLite-backed via SQLModel)
- Memory Stream nodes (observation-based, embeddings, importance scoring)
- Built-in tools: web search, filesystem, execute command, run Python
- Jinja2 template system for agent system prompts
- Scheduled events (timer-triggered autonomous operation)
- Integrated local TTS (Piper, 150+ voices) and STT (faster-whisper, wake word)
- Docker Compose deployment
- Mobile-optimized web UI at `/mobile`

---

## Architecture Highlights

**Backend stack:** Flask + SocketIO + SQLite/SQLModel + LiteLLM

**Memory architecture — two-tier:**
1. `KnowledgeGraph` — persistent entity-relationship graph (entities, properties, relationships). Agents write to it via tools (AddEntity, AddRelationship, QueryEntities). Long-term structured memory.
2. `MemoryStream` — observation buffer with embeddings for semantic recall. Messages/tool calls/responses are embedded and stored immediately; retrieved by cosine similarity. Has an importance threshold + reflection mechanism (summarization at intervals).

**Agent runtime:** Pure Python asyncio, agents run as graph nodes connected by typed edges (message, pipeline, resource, delegate). The graph engine walks topology, delivers messages, and handles tool call cycles.

**LLM access:** Unified via LiteLLM — runs against llama.cpp, Ollama, OpenAI, Anthropic, any compatible endpoint.

---

## Relevance to West AI Labs / Nebulus Stack

**High relevance.** This is the closest open-source analog to what Nebulus-Gantry is trying to become:

- Local-first ✅
- Visual workflow editor — Nebulus doesn't have this yet; worth watching for UI inspiration
- Two-tier memory (graph + stream) mirrors what we've discussed for Nebulus-Core memory layer
- Knowledge graph via SQLite (no heavy dependencies) — Nebulus currently leans on ChromaDB + NetworkX; this shows a leaner path
- Jinja2 agent templates — matches our template-based prompt approach
- Docker Compose deployment — aligns with container-first Nebulus architecture
- Scheduled autonomous events — relevant to Nebulus-Gantry's orchestration scheduler

**Gaps vs. Nebulus:** No MCP support, no multi-node/distributed agents (single-process), no GPU inference integration, Flask (not FastAPI). But the visual layer and memory architecture are worth deep study.

---

## Recommended Next Steps

1. **Study the memory module** (`backend/beezle_bug/memory/`) — knowledge_graph.py and memory_stream.py are directly applicable to Nebulus-Core memory design
2. **Look at agent_graph/** — understand how the graph engine routes messages and manages tool call cycles
3. **Consider the visual editor** — React Flow-inspired but custom; this could inform a future Nebulus-Gantry UI
4. **Watch for updates** — project is actively evolving (2 years old, still pushing commits)
5. Don't adopt as-is: Flask + SQLite limits scale, no auth, no MCP. But the ideas are solid.
