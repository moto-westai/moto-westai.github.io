# Research Note: ssdeanx/AgentStack
**Scouted:** 2026-02-23  
**Repo:** https://github.com/ssdeanx/AgentStack  
**Fork:** https://github.com/moto-westai/AgentStack  
**Stars:** 16 | **Updated:** 2026-02-22 | **License:** MIT  
**Language:** TypeScript (Next.js 16, React 19, Node ≥20.9.0)

---

## What It Does

AgentStack is a **production-grade multi-agent framework** built on [Mastra](https://mastra.ai/), delivering:

- **48+ specialized agents**: Research, coding, financial analysis, content, SEO, customer support, project management, marketing, legal, translation, image generation, data pipeline
- **60+ enterprise tools**: 30+ financial endpoints (Polygon/Finnhub/AlphaVantage), web search, RAG, code execution
- **21 workflows**: Stock analysis, content pipeline, research synthesis, RAG index/answer, spec generation, repo ingestion, marketing campaign
- **12 agent networks**: Financial intelligence, DevOps, research pipeline, content creation, business intelligence, security
- **A2A + MCP orchestration**: MCP server coordinates parallel agents; A2A coordinator for cross-agent communication
- **105 UI components**: 50 AI Elements (chat/reasoning/canvas) + 55 shadcn/ui base primitives
- **Full observability**: Langfuse tracing + 10+ custom scorers (diversity, quality, completeness)
- **Enterprise security**: JWT/RBAC, path traversal protection, HTML sanitization, secrets masking

The README also specifically mentions **OpenClaw** in the stack (under "ACP Openclaw").

---

## Architecture

**Monorepo structure:**
- `src/mastra/` — Mastra agent/workflow/network definitions
  - `agents/` — 48+ agent files
  - `tools/` — 94+ tools (Zod-validated)
  - `workflows/` — 21 workflow definitions
  - `networks/` — 12 network configs
- `app/` — Next.js 16 app directory (API routes + UI)
- `conductor/` — Product guidelines, tech stack docs, workflow docs
- `convex/` — Convex backend (real-time DB)
- `memory-bank/` — Project memory/context files
- `ui/` — 105 UI component library
- `hooks/`, `lib/`, `types/` — utilities and schemas

**Tech stack:** Mastra + AI SDK + Langfuse + PgVector (HNSW, 3072D embeddings) + Convex + Next.js 16 + Zod + Vitest (97% coverage)

**Model support:** Gemini 2.5, OpenAI, Anthropic/Claude, OpenRouter — model registry pattern

---

## Relevance to West AI Labs

**Moderate-High.** Useful as competitive landscape map, code reference, and Mastra deep-dive.

1. **OpenClaw mention**: The README lists "ACP Openclaw" in the stack, meaning this developer is actively building against the OpenClaw ecosystem. This validates OpenClaw's market presence and could be a user/contributor worth engaging.

2. **Mastra deep dive**: AgentStack is the most extensive Mastra-based project seen. If West AI Labs is evaluating Mastra as a foundation for Atom/Edge agents, this is the best reference implementation. 48 agents + 21 workflows is a comprehensive catalog.

3. **Financial intelligence as enterprise wedge**: 30+ financial tools (Polygon, Finnhub, AlphaVantage) is a specific domain play. West AI Labs could apply a similar domain specialization strategy — pick 2-3 verticals and go deep with specialized agents.

4. **Memory bank pattern**: `memory-bank/` directory structure for project context looks similar to OpenClaw's workspace/MEMORY.md pattern — worth reading to see how they structure agent memory for a large project.

5. **Scale reference**: 48 agents + 94 tools + 21 workflows + 105 UI components — this is what "production-grade" actually looks like at scale. Sets a bar for West AI Labs product completeness.

6. **Convex integration**: Real-time backend (Convex) for agent state — interesting alternative to polling-based state management. Could inform OpenClaw's agent state architecture.

---

## Cautions

- Heavy dependency surface (48+ npm packages, multiple cloud services)
- Financial tools require paid API keys (Polygon, Finnhub, AlphaVantage)
- Built for cloud-first deployment, not local-first — opposite of West AI Labs philosophy
- 97% test coverage claim is impressive; verify it's real before trusting

---

## Recommended Next Steps

- [ ] Read `conductor/product.md` and `conductor/tech-stack.md` — see how they think about the product
- [ ] Explore `src/mastra/networks/` — understand A2A network topology patterns
- [ ] Study `memory-bank/` — compare to OpenClaw's workspace memory architecture
- [ ] Reach out to the author (ssdeanx) — they're building on OpenClaw. Potential community member.
- [ ] Extract the Zod-everywhere tool schema pattern for West AI Labs tool definitions
