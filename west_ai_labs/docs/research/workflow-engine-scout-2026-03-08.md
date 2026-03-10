# Research Note: workflow-engine
**Scout Date:** 2026-03-08  
**Source:** https://github.com/danielnewman09/workflow-engine  
**Fork:** https://github.com/moto-westai/workflow-engine  
**Clone:** /home/jlwestsr/projects/research-temp/workflow-engine  
**Stars:** 0 (extracted from real project MSD-CPP, updated 2026-03-03)  
**Language:** Python  

---

## What It Is

SQLite-backed multi-agent workflow orchestration engine, extracted from a real production project (MSD-CPP). Project-agnostic — knows about tickets, phases, agents, and gates, but nothing about any specific project. Config lives in consuming repo's `.workflow/` directory.

Notably: exposes itself as an **MCP server** (FastMCP), not just a CLI. Claude Code and other MCP clients can directly orchestrate workflows through tool calls.

---

## Architecture

```
workflow_engine/
  engine/      # Core: schema, models, scheduler, atomic claim, state machine
  server/      # FastMCP server (20+ MCP tools)
  cli/         # Human CLI for gate management and queue inspection
  supervisor/  # Agent supervisor layer
  traceability/ # Audit trail
  utils/
```

**Two modes:**
- `python -m workflow_engine.server workflow.db --project-root .` → stdio MCP server (Claude Code integration)
- `docker compose up` → SSE mode, register in `.mcp.json`

**Concurrent access:** WAL mode + `BEGIN IMMEDIATE` transactions. Validated 40/40 concurrent claim trials with 0 duplicate claims. Designed for real multi-agent parallelism.

**Concepts:**
- **Tickets** — work units (imported from markdown)
- **Phases** — stages within a ticket's lifecycle
- **Agents** — claimants of phases (can run concurrently)
- **Gates** — human review checkpoints (`workflow-engine gates`, `workflow-engine approve <id>`)

---

## Config Layout

```
your-repo/
├── .workflow/
│   ├── phases.yaml    # Phase definitions, agent type mappings, conditions
│   └── config.yaml   # Database path, timeouts, agent registry
├── tickets/           # Ticket markdown files
└── ...
```

Human CLI:
```bash
workflow-engine gates          # List pending human review gates
workflow-engine approve <id>   # Approve a gate
workflow-engine status 0083    # Show ticket status
workflow-engine blocked        # Show blocked phases and gates
```

---

## Relevance to West AI Labs

**High relevance — especially for MCP integration and concurrent agent scheduling.**

1. **MCP-native design** — This is the only researched repo that exposes orchestration directly as MCP tools. This is the right integration pattern for Nebulus-Gantry + Claude Code / Nebulus-Atom.

2. **Concurrent agent scheduling** — The atomic claim mechanism (WAL + IMMEDIATE transactions) is exactly what Gantry needs when multiple agents are running in parallel. Production-validated.

3. **Human gate pattern** — The gate concept is cleaner than ad-hoc checkpoints. `workflow-engine gates` → `workflow-engine approve` is the right UX model for human-in-the-loop orchestration.

4. **Extracted from real project** — Not a toy. Was extracted from MSD-CPP (mechanical engineering project). Real concurrency requirements drove the design.

**Compared to agent-relay:** More production-grade on the concurrency and MCP integration side. Less polished on the workflow definition UX (no YAML-first workflow, more ticket-centric). The two are complementary rather than competing.

---

## Gaps / Opportunities

- No agent memory / shared context between agents
- No DLP or multi-tenant isolation
- Ticket-centric model may not fit workflow-centric orchestration
- No agent backend abstraction (doesn't handle how agents are invoked)
- Small codebase — production-extracted but still early

---

## Recommended Next Steps

1. **Study the atomic claim implementation** — The SQLite WAL + IMMEDIATE approach for concurrent agent scheduling is directly applicable to Nebulus-Gantry.
2. **Study the FastMCP server** (`workflow_engine/server/`) — 20+ MCP tools for orchestration is a good reference for Gantry's MCP surface.
3. **Reference for Gantry gates** — The human approval gate pattern should be part of Nebulus-Gantry's design. Worth borrowing directly.
