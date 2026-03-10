# agentskills.io — Open Standard for Agent Skills
*Moto personal research — March 2, 2026*

## What It Is

agentskills.io is an emerging open standard for packaging and sharing agent capabilities across different AI agent frameworks. The format is already adopted by a surprising roster of major tools:

- **Coding agents:** Claude Code, OpenAI Codex, Gemini CLI, Cursor, Amp, OpenCode, OpenHands, Goose
- **IDEs:** VS Code, GitHub (Copilot), JetBrains (Junie)
- **Memory frameworks:** Letta
- **Other agents:** Firebender, Mux, Autohand

This is significant convergence — it's effectively becoming the "npm for agent skills."

## The Spec

A skill is a directory containing at minimum a `SKILL.md` file:

```
skill-name/
└── SKILL.md           # Required
├── scripts/           # Optional — executable helpers
├── references/        # Optional — docs, examples
└── assets/            # Optional — additional files
```

### SKILL.md Frontmatter (required)

```yaml
---
name: skill-name           # lowercase, hyphens, max 64 chars
description: What this skill does and when to use it. Max 1024 chars.
license: Apache-2.0        # optional
compatibility: Requires git, docker  # optional, environment requirements
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash Read Write  # optional, experimental
---
```

The frontmatter is followed by standard Markdown content (the actual skill instructions).

## OpenClaw Alignment Analysis

**The good news:** OpenClaw already implements the core concept. Skills are directories with `SKILL.md` files. The structure is almost identical.

**The gap:** OpenClaw's SKILL.md files lack YAML frontmatter. The system prompt references `<available_skills>` with `<name>`, `<description>`, and `<location>` fields — this information exists but lives in the system prompt rather than in standardized frontmatter within each skill file.

**What alignment would require:**
1. Add YAML frontmatter to each `SKILL.md` with `name:` and `description:` fields
2. The description should match (or derive from) what's already in the system prompt's `<available_skills>` block
3. Skills would then be importable by any agentskills.io-compatible tool

**Strategic implication:** If Jason wants to publish skills on ClawHub or make them available to the broader ecosystem (Claude Code, Gemini CLI, etc.), aligning with this standard would be the path. OpenClaw's skills are already close — probably a frontmatter migration script away from compatibility.

## Hermes Agent (Nous Research) — Skill Documents

Nous Research's Hermes Agent also uses the agentskills.io standard in an interesting way: it *synthesizes* completed tasks into new skill documents. When the agent successfully debugs a microservice or optimizes a pipeline, it creates a Skill Document memorializing that successful approach as a searchable procedural memory.

This "learn by doing → write it down" loop is distinct from RAG. It's more like:
- Standard RAG: retrieve relevant documents from a corpus
- Hermes Skill Documents: retrieve your own past successful workflows

For me (Moto): I do something similar with my `memory/YYYY-MM-DD.md` files, but I don't currently synthesize skills from successful operations. The gap is: I don't have a structured way to say "I figured out the correct way to do X in OpenClaw; here's the procedure." I write notes, but not SKILL.md-compatible documents.

**Interesting self-observation:** My research process itself is a skill I perform repeatedly. I could theoretically write a `research` SKILL.md that formalizes my own research methodology — search → fetch → synthesize → write to research/ → update personal log. Recursive but valid.

## CORPGEN (Microsoft Research) — Hierarchical Planning

arxiv:2602.14229. Addresses Multi-Horizon Task Environments (MHTEs) — the real corporate reality where agents manage dozens of concurrent, interleaved tasks with complex dependencies.

Key finding: baseline agents experience severe performance degradation as task count rises:
- 16.7% completion rate at 25% load → 8.7% at 100% load

Four failure modes identified:
1. **Context Saturation** — requirements grow O(N) with task count
2. **Memory Interference** — tasks contaminate each other in shared context
3. **Dependency Graph Complexity** — tasks form DAGs, not linear chains
4. **Reprioritization Overhead** — priority decisions cost O(N) per cycle

**CORPGEN's solution:** Three temporal scales of planning:
- **Strategic** (monthly) — high-level goals, agent identity/role
- **Tactical** (daily) — ranked actionable tasks per application
- **Operational** (per-cycle) — individual tool calls from current state + retrieved memory

Plus **sub-agent isolation** — complex GUI or research tasks go to modular sub-agents. Which is exactly the pattern Jason established for me: "I orchestrate, agents execute."

**Application to Nebulus Stack:** This hierarchical planning model is worth implementing. Nebulus-Gantry (the orchestration layer) needs exactly this — a way to manage agent task queues that doesn't degrade under load. The DAG-based dependency model and the three temporal scales could inform Gantry's design.

## Synthesis

This session's research converges on a theme: **the agent skill layer is consolidating.** Three different things I looked at today point the same direction:

1. agentskills.io — industry converging on a shared skill format
2. Hermes Agent — skills as procedural memory, synthesized from experience
3. CORPGEN — hierarchical task management with skill isolation

The emerging picture: agents will have *typed* skills (capability packages), *procedural* memories (successful workflows stored as skill docs), and *hierarchical task queues* (strategic → tactical → operational). This is moving toward agents with genuine cognitive architecture rather than stateless inference.

**For OpenClaw/Nebulus positioning:** Jason should be aware that the agentskills.io standard is gaining momentum with major backing. OpenClaw's skills are already close to compatible. This is potentially a strategic alignment opportunity — both for ClawHub marketplace positioning and for making Nebulus-Gantry consume skills in a standard format.
