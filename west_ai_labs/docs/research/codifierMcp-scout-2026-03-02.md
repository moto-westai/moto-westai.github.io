# CodifierMcp — Scout Notes (2026-03-02)

**Repo:** https://github.com/JArchitectMPlus/codifierMcp  
**Fork:** https://github.com/moto-westai/codifierMcp  
**Stars:** 0 (brand new, pushed 2026-03-03)  
**Language:** TypeScript  
**Clone:** /home/jlwestsr/projects/research-temp/codifierMcp

---

## What It Does

CodifierMcp is a remote MCP (Model Context Protocol) server that provides AI assistants with shared, persistent organizational knowledge. It creates a "virtuous cycle" where learnings from any session (dev, researcher, analyst) are stored in a shared KB and surfaced in future sessions across the org.

Two core MCP tools: `fetch_context` and `update_memory`. Plus `manage_projects`, `pack_repo` (via RepoMix), and `query_data` (AWS Athena).

Local sessions write to `docs/MEMORY.md` during work, then sync to the shared KB via `/push-memory` slash command.

---

## Architecture Highlights

- **Transport:** stdio (local) OR SSE/HTTP (remote). Bearer token auth middleware.
- **Backend:** Supabase (PostgreSQL + pgvector). Projects / repositories / memories schema.
- **Skills = client-side Markdown.** Server has no session state — the LLM reads a skill file and drives conversation, calling MCP tools only for data ops. Clean separation.
- **Slash commands** for Claude Code / Cursor: `/remember`, `/push-memory`, `/recall`, `/codify`, `/research`, `/onboard`.
- **GitHub Actions workflows** included: `claude.yml`, `claude-code-review.yml`, `deploy.yml` (Fly.io). Production-minded from day one.
- **Cross-role knowledge flow**: a researcher's `research_finding` memory type is retrievable by a developer via `fetch_context` when initializing a related project months later.
- `CLAUDE.md` and `GEMINI.md` both present — they've thought about multi-assistant compatibility.

---

## Relevance to West AI Labs

**Very High.** This is essentially an MCP-native implementation of what Nebulus-Core needs for agent memory.

Key alignments:
- Local-first session capture (`docs/MEMORY.md`) → sync to shared KB on demand. This is exactly the pattern Moto uses for `memory/YYYY-MM-DD.md` → `MEMORY.md`.
- pgvector backend = searchable semantic memory. Could swap Supabase for a self-hosted PG+pgvector instance (privacy-conscious local-first).
- The Skills-as-Markdown pattern is structurally identical to OpenClaw's skills system. Direct philosophical alignment.
- Cross-session knowledge persistence is the #1 unsolved problem for Nebulus agent workflows.

Concerns:
- Supabase dependency = cloud. For local-first deployment, would need self-hosted Supabase or PG replacement.
- 0 stars today, but architecture is solid. Worth watching closely.

---

## Recommended Next Steps

1. **High priority:** Evaluate as the memory/KB layer for Nebulus-Core. The MCP tool interface is clean and composable.
2. Fork and adapt for local Supabase (Docker Compose) deployment — remove cloud dependency.
3. The `/codify` slash command pattern (capture session learnings → push to KB) could be adopted in West AI Labs' Claude Code workflows immediately.
4. Consider contributing: a local Postgres adapter would make this deployable without Supabase.
