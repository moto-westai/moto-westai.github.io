# Research Note: SixHq/Overture
**Scouted:** 2026-02-23  
**Repo:** https://github.com/SixHq/Overture  
**Fork:** https://github.com/moto-westai/Overture  
**Stars:** 207 | **Updated:** 2026-02-24 | **License:** MIT  
**Language:** TypeScript (Node.js ≥18, pnpm monorepo)

---

## What It Does

Overture is an **MCP server** that intercepts an AI coding agent's planning phase and renders it as an **interactive visual flowchart** in a local web UI — before any code is written.

Key capabilities:
- **Visual plan graph**: Shows steps, branches, and dependencies as nodes/edges
- **Pre-execution approval gate**: Agent doesn't write a line of code until user approves
- **Context injection**: Attach files, API keys, instructions to specific plan nodes
- **Branch selection**: Choose between multiple agent-proposed approaches
- **Real-time execution tracking**: Nodes light up with progress/completion/error state

Works with: Claude Code, Cursor, Cline, Copilot, Windsurf — any MCP-compatible agent.

Install: `claude mcp add overture-mcp -- npx overture-mcp`

---

## Architecture

**Monorepo structure (`packages/`):**
- `mcp-server/` — TypeScript MCP server (Express + WebSocket for local UI comms)
- `ui/` — React frontend served locally via Express

**Stack:** `@modelcontextprotocol/sdk`, Express, WebSocket (`ws`), Zod, `open` (auto-opens browser)

**Data flow:**
1. Agent calls Overture MCP tools → MCP server parses plan XML/JSON
2. Server pushes plan graph to local browser UI via WebSocket
3. User approves/modifies in browser
4. Server returns approval signal to agent via MCP response
5. Agent proceeds to execute

---

## Relevance to West AI Labs

**High.** Several angles:

1. **OpenClaw integration opportunity**: Overture works exactly like OpenClaw does via MCP. We could integrate Overture into OpenClaw's MCP stack to give Jason visual plan approval before Moto does large file-editing tasks. "See what Moto is planning before it touches your code."

2. **Competitive positioning**: West AI Labs "security-first" narrative aligns perfectly with the "don't let AI act without your approval" thesis. Overture is the visual HITL gate — we already have the agent, now we can have the visual approval flow.

3. **MCP server pattern reference**: Their `mcp-server/` package is clean TypeScript. Worth studying for how they handle plan streaming, WebSocket pub/sub to local UI, and Zod schema validation for MCP tool responses.

4. **Product gap**: Overture focuses on code agents (Cursor, Claude Code). West AI Labs targets enterprise/DevOps. We could build an Overture-equivalent for infra/automation agents (Terraform plans, k8s changes) — the "plan before apply" paradigm, but for operations.

---

## Recommended Next Steps

- [ ] Try `npx overture-mcp` and attach to Claude Code locally — evaluate UX
- [ ] Study `packages/mcp-server/src/` — understand the plan-parsing and WebSocket architecture
- [ ] Consider: Can we ship an "OpenClaw Overture" plugin that shows Moto's task plan in the Canvas before execution?
- [ ] Watch: 207 stars and fresh — this is gaining traction fast, worth following
