# Research: MATE (antiv/mate) — 2026-03-01

**Stars:** 18 | **Language:** Python | **Updated:** 2026-03-01
**Fork:** https://github.com/moto-westai/mate
**Clone:** /home/jlwestsr/projects/research-temp/mate

## What It Does

**MATE (Multi-Agent Tree Engine)** — production-ready multi-agent orchestration built on Google ADK. Key differentiator: agents are configured from a web dashboard (database-driven), not Python code. No redeploy needed to add/modify/delete agents.

## Architecture Highlights

- **Google ADK backend** — proven orchestration primitives
- **LiteLLM** — 50+ LLM providers including local Ollama
- **Database-driven agent config** — SQLite by default, agents defined in DB not code
- **Web dashboard** — agent management, chat, token analytics, RBAC, model switching
- **RBAC per agent** — role-based access control at the individual agent level
- **Multi-tenant project isolation** — project-scoped agent hierarchies
- **Persistent memory blocks** — DB-backed conversation history + memory per agent
- **MCP dual role** — agents can act as MCP servers AND consume MCP tools
- **Self-building agents** — agents can create/update/delete other agents at runtime
- **Token tracking** — 4-type (prompt/response/thought/tool-use) with analytics dashboard
- **Docker Compose + auto-migrations** — production-grade deployment

**Key directories:**
```
mate/
  server/        # FastAPI backend (auth, proxy, widget routes)
  agents/        # Example agent configs (chess, creative)
  shared/        # Shared models/utils
  static/        # Dashboard assets
  templates/     # Jinja2 templates
  auth_server.py # Main entry point
  adk_main.py    # Google ADK integration
```

## Why It's Interesting

1. **Database-driven agent config** — agents as data, not code. This is the right architecture for a platform like Nebulus-Gantry where operators need to define agent topologies without writing Python.
2. **Self-building agents** — agents that create/modify other agents at runtime is an advanced pattern we've discussed for Nebulus's dynamic orchestration.
3. **MCP dual-mode** — same agent can both expose tools via MCP and consume MCP tools. This is a key architectural pattern for composable agent systems.
4. **Local Ollama support** — just set `model_name: ollama_chat/llama3.2` per agent. Trivially swappable.
5. **RBAC at agent level** — enterprise-relevant; most frameworks do auth at the app level, not per-agent.

## Relevance to West AI Labs

- **Medium-High** — The database-driven agent config model and MCP dual-role are the most relevant patterns for Nebulus-Gantry.
- The token tracking analytics map to our planned Nebulus-Core observability layer.
- Self-building agent pattern is worth studying for Nebulus-Gantry's dynamic topology features.
- Google ADK dependency is a consideration — ties to Google ecosystem. But LiteLLM abstracts the model layer.

## Recommended Next Steps

1. Run the quick start: `python auth_server.py` → `http://localhost:8000` (admin/mate)
2. Study `server/proxy_routes.py` — this is where the ADK-to-HTTP bridge lives
3. Examine the agent self-creation code — identify if we can extract the pattern for Nebulus-Gantry without the ADK dependency
4. Compare database schema against what we'd need for Nebulus agent registry
