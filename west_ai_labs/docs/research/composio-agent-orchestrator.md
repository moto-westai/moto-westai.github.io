# Research: ComposioHQ/agent-orchestrator
**Analyzed:** 2026-02-21 | **Source:** https://github.com/ComposioHQ/agent-orchestrator  
**Analyst:** Moto | **Relevance:** Nebulus-Gantry, Moto Workforce, multi-agent architecture

---

## What It Is

Agent Orchestrator manages fleets of AI coding agents working in parallel on a codebase. Each agent gets its own git worktree, its own branch, and its own PR. When CI fails, the agent fixes it. When reviewers leave comments, the agent addresses them. You only get pulled in when human judgment is required.

**Agent-agnostic** (Claude Code, Codex, Aider) · **Runtime-agnostic** (tmux, Docker, k8s) · **Tracker-agnostic** (GitHub, Linear)

This is purpose-built for coding teams — not general AI infrastructure. But the architecture is worth studying closely.

---

## Architecture: The 8 Plugin Slots

Every abstraction is swappable via a plugin interface. All defined in `types.ts`.

| Slot | Default | Alternatives | Interface |
|------|---------|-------------|-----------|
| **Runtime** | tmux | docker, k8s, process | `Runtime` |
| **Agent** | claude-code | codex, aider, opencode | `Agent` |
| **Workspace** | worktree | clone | `Workspace` |
| **Tracker** | github | linear | `Tracker` |
| **SCM** | github | — | `SCM` |
| **Notifier** | desktop | slack, webhook | `Notifier` |
| **Terminal** | iterm2 | web, none | `Terminal` |
| **Lifecycle** | core | (not pluggable) | `LifecycleManager` |

Plugin contract is minimal: implement the interface, export a `PluginModule`. That's the entire integration surface.

---

## Session State Machine

Sessions are proper state machines with 15 states and meaningful transitions:

```
spawning → working → pr_open → ci_failed → working (auto-fix)
                   ↓         ↓
              review_pending → changes_requested → working (auto-fix)
                   ↓
              approved → mergeable → merged
                   ↓
         needs_input / stuck / errored → (human notification)
```

This is production-grade. The `ci_failed → auto-fix → pr_open` loop is the key automation value — agents self-correct without human involvement.

**ActivityState** is separate from SessionStatus:
- `active` — agent is processing
- `ready` — agent finished turn, waiting for input
- `idle` — inactive (stale)
- `waiting_input` — agent asking for permission/clarification
- `blocked` — hit an error
- `exited` — process dead

Two orthogonal axes: lifecycle status + agent activity. Smart.

---

## The Reaction Engine

The lifecycle manager has an **automatic reaction system**:

```yaml
# agent-orchestrator.yaml
reactions:
  ci.failed:
    auto: true
    action: send-to-agent
    message: "CI is failing. Fix the issues."
    retries: 3
    escalateAfter: 2h

  review.changes_requested:
    auto: true
    action: send-to-agent
    message: "Review requested changes. Address them."
    retries: 2
    escalateAfter: 4h

  session.stuck:
    auto: true
    action: notify
    priority: urgent
```

This is the key pattern: **declare what to do when things happen, not how to do them.** The lifecycle manager polls for state changes and fires the appropriate reaction. Human only gets interrupted when auto-handling fails or escalation threshold is hit.

---

## Convention Over Configuration

Config is minimal by design. Three required fields per project:

```yaml
projects:
  - path: ~/repos/myapp      # Where is the repo?
    repo: org/myapp          # GitHub owner/repo
    defaultBranch: main      # Base branch
```

Everything else is auto-derived:
- **Project ID**: `basename(path)` 
- **Session prefix**: generated from project name (e.g., `agent-orchestrator` → `ao`)
- **Namespacing**: SHA256 hash of config directory path (12 chars) prevents multi-instance collisions
- **Storage**: `~/.agent-orchestrator/{hash}-{projectId}/sessions|worktrees|archive/`

No path config. No ID config. No namespace config. Just the essentials. This is a significant UX insight.

---

## Multi-Agent Hierarchy

There's an **orchestrator agent** that manages **worker agents**:

- Orchestrator: spawned via `ao spawn-orchestrator` — a Claude Code session that has `CLAUDE.orchestrator.md` injected with full context about the project, available commands, and reaction patterns. It doesn't write code — it manages workers.
- Workers: spawned by orchestrator or human via `ao spawn <project> <issue>` — each gets their own worktree, branch, and full issue context. They write code, open PRs, respond to reviews.

The orchestrator is itself an AI agent. It reads `ao status`, decides what to spawn next, monitors workers, and intervenes when needed. **An AI managing AIs.** This is the Moto Workforce architecture.

---

## Competitive Landscape (Their Own Research)

They analyzed 16+ projects before building. Key players:

**Gas Town (Steve Yegge)** — Most ambitious. Go 1.23+, ~189K LOC, MEOW stack (Molecular Expression of Work). 7 agent roles: Mayor, Deacon, Dogs, Crew, Polecats, Refinery, Witness. Uses "Beads" (JSONL in Git) as coordination plane. Crash-recovery built in. Con: ~$100/hr token burn, auto-merges failing tests, Go-only ecosystem.

**Par (Coplane)** — Python, closest to their approach. Single-command UX (`par start my-feature`). Broadcast to all sessions (`par send all "<cmd>"`). Unified control center.

**Loki Mode** (we studied this one too) — 90K lines, requires `--dangerously-skip-permissions`, $100-1000+ per project.

**Key gap they found and filled:** Everything else is either too complex (Gas Town), too bare-bones (Par), or too expensive (Loki Mode). Agent Orchestrator hits the middle: opinionated defaults, swappable internals, dashboard, reaction engine.

---

## What's Relevant to West AI Labs

### Nebulus-Gantry
The plugin slot architecture is directly applicable. Gantry's orchestration layer should have swappable runtime, agent, workspace, tracker, and notifier slots — not hardcoded integrations. The `types.ts` interface definitions are worth studying as a reference implementation.

### Reaction Engine Pattern
The `reactions` config block is a product insight: operators shouldn't write event handlers, they should declare policies. `ci.failed → send-to-agent → escalate-after-2h` is a three-field config that replaces what would be 50 lines of event handler code. This maps to Nebulus-Atom's scheduled tasks pattern.

### Session State Machine
The 15-state machine + separate ActivityState is the right model for tracking AI agent sessions. Terminal/non-terminal states, restorable vs non-restorable — clean. Worth adopting this model in Gantry rather than building from scratch.

### Moto Workforce
The orchestrator-manages-workers pattern is the Moto Workforce architecture. Orchestrator AI gets injected context via `CLAUDE.orchestrator.md` and issues `ao spawn` / `ao send` commands. Workers operate in isolation. This is exactly the "Employees That Ship in a Box" model — each worker is an isolated session with its own branch and context.

### Hash-Based Namespacing
The SHA256(configDir) → 12-char prefix approach to prevent multi-instance collisions is a solved problem worth reusing. Simple, deterministic, zero-config.

---

## What's NOT Relevant

- **GitHub dependency**: Everything flows through GitHub Issues/PRs/CI. Local-first doesn't apply here — they assume cloud.
- **Coding-only scope**: Built exclusively for "implement GitHub issues" use case. Not general AI infrastructure.
- **No local model support**: Assumes Claude Code / Codex / Aider with cloud API keys.
- **No privacy posture**: All logs, branches, PRs go to GitHub. Not suitable for sensitive codebases.

---

## Should We Fork?

**For Gantry:** No — different scope. But extract patterns:
1. Plugin slot interface definitions from `types.ts`
2. Session state machine design
3. Reaction engine declarative config format
4. Hash-based namespacing

**For coding-specific use cases:** Maybe. If a customer needs "spawn 10 coding agents on my GitHub issues," this is the off-the-shelf answer. We'd fork, add local model support (TabbyAPI/MLX backend), and strip the cloud dependency.

**For product positioning:** Good competitive data point. We're building the infrastructure layer that makes something like this possible locally. Agent Orchestrator is a product built on top of what we're building.

---

## Recommended Next Steps

1. Fork to `westailabs/agent-orchestrator-fork` on GitHub — preserves our ability to contribute/adapt
2. Extract `types.ts` plugin interfaces as reference for Gantry's plugin architecture
3. Map Agent Orchestrator's "project" to Gantry's "conductor track" — they're analogous
4. Spike: add TabbyAPI/Ollama as an `Agent` plugin — proof of concept for local-model support

---

*Cloned to: `~/projects/agent-orchestrator`*  
*Research output: this file*
