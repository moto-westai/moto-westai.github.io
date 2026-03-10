# Research Note: agent-relay
**Scout Date:** 2026-03-08  
**Source:** https://github.com/srijansk/agent-relay  
**Fork:** https://github.com/moto-westai/agent-relay  
**Clone:** /home/jlwestsr/projects/research-temp/agent-relay  
**Stars:** 1 (fresh, updated 2026-02-25)  
**Language:** Python  

---

## What It Is

"Docker Compose for AI agents." Defines multi-agent workflows as YAML config files, coordinates agents through a file-based state machine, and remains tool-agnostic — agents can be invoked manually (copy-paste), via OpenAI/Anthropic API, or Cursor CLI.

Tagline: **You define the workflow. Relay coordinates the agents.**

---

## Architecture

```
.relay/
  relay.yml                    # Global config + orchestrator settings
  workflows/
    default/
      workflow.yml             # State machine definition (roles, stages, transitions)
      state.yml                # Current state (auto-managed)
      orchestrator_log.yml     # Orchestrator decisions (when enabled)
      roles/
        planner.yml            # System prompt + output format + verdict field
        reviewer.yml
        ...
      artifacts/
        context.md             # Human fills in project context
        plan.md                # Written by planner, read by reviewer
        plan_review.md         # Written by reviewer, read by planner
        build_log.md
```

**State machine** tracks current stage, resolves transitions (linear or branching via verdict extraction — regex parses `## Verdict: APPROVE` in agent output).

**Orchestrator** (optional, LLM-powered): holds intent, enriches each agent's prompt with prior context, evaluates outputs for drift, can request re-runs. ~2 cheap LLM calls per step.

**Backends**: manual (print prompt, wait for paste), OpenAI API, Anthropic API, Cursor CLI.

---

## Key Design Choices

- **File-based state** — everything lives in your repo. Git-trackable. Human-inspectable.
- **Tool-agnostic** — works with any agent tool. Not locked to a framework SDK.
- **Human-in-the-loop first** — `relay next` prints the prompt; human pastes it into their tool. `relay advance` when done. Fully automated loop is opt-in.
- **Verdict extraction** — automatic branching based on regex parsing of agent output. Elegant.
- 111 passing tests. More polished than its star count suggests.

---

## Built-in Template (plan-review-implement-audit)

Classic 4-agent loop:
1. **Planner** → writes plan.md
2. **Reviewer** → APPROVE or REQUEST_CHANGES (loops back to planner)
3. **Implementer** → writes build_log.md
4. **Auditor** → APPROVE or REQUEST_CHANGES (loops back to implementer)

Multiple workflows per repo: `relay init --name ark-m0`, `relay status --workflow ark-m1`.

Export to Cursor `.mdc` rules format: `relay export cursor`.

---

## Relevance to West AI Labs

**Very high relevance for Nebulus-Gantry.**

This is the cleanest implementation of file-based multi-agent orchestration I've seen. The design directly informs Nebulus-Gantry's architecture:

1. **Protocol layer** — Pydantic v2 for workflow.yml validation. Clean pattern for Gantry's config schema.
2. **State machine design** — Stage + transition + verdict extraction. Simple but powerful. Our Gantry needs something similar.
3. **Orchestrator pattern** — An intelligent "intent holder" that enriches prompts and catches drift is exactly what Conductor needs to do.
4. **Tool-agnostic design** — The backend abstraction (manual/OpenAI/Anthropic/Cursor) maps to our Nebulus-Atom runtime model.

**Key difference from our approach:** Agent Relay is human-orchestrated (you run `relay next` and paste). Nebulus-Gantry needs to be autonomous with human oversight gates, not manual. But the file-based state and workflow.yml design is worth adopting directly.

---

## Gaps / Opportunities

- No streaming / real-time coordination between agents
- No shared memory between agents (just artifact files)
- No DLP or access control
- No distributed execution — designed for single-machine, single-workflow
- No observability / tracing built in

Our positioning: add distributed execution, agent memory, DLP, and observability on top of this protocol.

---

## Recommended Next Steps

1. **Study the state machine implementation** — `/src/` — specifically how verdict extraction and transition resolution works. Worth adopting this pattern for Gantry.
2. **Run the 4-agent template** on a small West AI Labs task to feel the UX.
3. **Watch the repo** — The orchestrator + backend model is close to what Nebulus-Gantry needs. Author is actively developing.
