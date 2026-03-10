# agent-streams — Research Note
**Date:** 2026-03-06
**Repo:** john-b-rush/agent-streams → fork: moto-westai/agent-streams
**Clone:** /home/jlwestsr/projects/research-temp/agent-streams
**Stars:** 5
**Language:** Python 3.11+
**License:** (check repo)

---

## What It Does

A **local CLI orchestrator** for long-running coding agents (Claude CLI by default) that enforces a review gate before any code gets merged. The core philosophy:

> "DONE is a claim, not a state."

The workflow: `Spec → Builder (Claude) → DONE → Overseer (Claude) → APPROVED | ISSUES.md → fix loop → merge`

Each "stream" runs in its own tmux session + git worktree. The builder runs until it believes it's done. The overseer — a separate Claude instance that never edits code — reviews the diff against the spec and either approves the merge or writes `ISSUES.md` for the builder to fix. This repeats until approval.

---

## Architecture Highlights

### Implementation
- **Single file**: `agent_streams.py` (2,081 lines) — self-contained, no framework deps beyond stdlib
- **tmux**: each stream gets its own named session for isolation and visibility
- **git worktrees**: streams work in isolated worktrees, preventing branch conflicts during parallel runs
- **State machine**: run state tracked via filesystem (`DONE`, `APPROVED`, `ISSUES.md` sentinel files)
- **Prometheus textfile metrics**: per-stream metrics written for scraping; lightweight dashboard at `:8765`

### Key Commands
```bash
agent-streams launch 3    # spawn 3 parallel builder streams in tmux
agent-streams status      # global run status (human or JSON)
agent-streams resume <id> # recover after tmux death
agent-streams merge <id>  # manual recovery for approved-but-not-merged
```

### Config
- `AGENT_STREAMS_HOME` — override home dir (default `~/.agent-streams/`)
- `AGENT_STREAMS_CLAUDE_BIN` — swap the agent binary (not locked to Claude)
- `AGENT_STREAMS_SESSION_PREFIX` — tmux session naming

### Prompts
Prompts live outside the repo: `~/.agent-streams/repos/<slug>/streams/streamN/prompt.md`
This means specs can be iterated without touching the repo.

---

## Relevance to West AI Labs

**Direct relevance to Nebulus-Atom** (runtime atoms) and **West AI Labs internal dev workflow**.

Specific overlap:
1. **Skeptical overseer pattern** — the builder/overseer separation is the right model for agentic code generation; a second agent that only reviews and never modifies is a key safety property we should bake into Conductor
2. **tmux + git worktree isolation** — practical, zero-infrastructure approach to parallel agent execution; relevant to Nebulus-Atom's execution model
3. **Filesystem state machine** — using sentinel files (`DONE`, `APPROVED`, `ISSUES.md`) for agent handoff is elegantly simple; no database, no message broker, fully inspectable by humans
4. **Pluggable agent binary** — not locked to Claude; the pattern works with any CLI agent, which matches our local-first philosophy
5. **Prometheus metrics** — even a single-file CLI tool has observability; reinforces our "metrics everywhere" standard

**The big idea to steal:** The overseer/builder split with a review gate. In Conductor, every code-generating agent should have a paired reviewer that enforces acceptance criteria before any output is committed. This is sound trust engineering.

**What it doesn't do:**
- No multi-machine distribution
- No dynamic spec generation (prompts are static files)
- No integration with CI/CD beyond git merge
- Single-user, local-only design
- No memory/context persistence between runs

---

## Recommended Next Steps

1. **Run it locally** — `./install.sh` and try a real task to feel the UX
2. **Read the overseer prompt handling** in `agent_streams.py` (~line 1000+) — understand how the review loop works
3. **Prototype a Conductor overseer node** based on this pattern — builder → DONE → reviewer → APPROVED/REJECT
4. **Consider adopting for West AI Labs internal dev** — we could use agent-streams today for complex refactors where Claude should have a review gate
5. **The single-file design** is a reference for Nebulus-Atom's minimal runtime footprint philosophy
