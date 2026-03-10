# Centaur — Scout Notes (2026-03-02)

**Repo:** https://github.com/EnderMio/Centaur  
**Fork:** https://github.com/moto-westai/Centaur  
**Stars:** 0 (brand new, pushed 2026-03-02)  
**Language:** Python  
**Clone:** /home/jlwestsr/projects/research-temp/Centaur

---

## What It Does

Centaur is a File-Driven, Stateless Multi-Agent Framework for software engineering tasks. It's built around a "human + AI" (半人马 = Centaur in Chinese) philosophy that explicitly rejects black-box memory graphs and instead uses Markdown files as the sole state carrier.

Three roles form the Triad:
- **Supervisor** — reads the big picture, maintains PLAN.md, dispatches TASK.md work orders. Never writes business code.
- **Worker** — executes only what's in TASK.md. Returns real data slices as acceptance evidence.
- **Validator** — cold red-team review. Catches hardcoded values, env coupling, contract violations. Has single-veto power.

---

## Architecture Highlights

- **State = Markdown files.** No DB, no memory graph. PLAN.md (kanban), TASK.md (agent comms bus), DESIGN.md, LESSONS.md, CODE_MAP.md, PROJECT_STATUS.md.
- **Stateless cold-start every time.** Each agent invocation re-reads file snapshots to rebuild context. Eliminates hallucination accumulation across long sessions.
- **Human acceptance gate** baked into the ROLE_ORDER: `supervisor → human_gate → worker → validator`. The system won't self-skip the gate.
- **Depends on `codex` CLI** (OpenAI Codex) as the execution engine — each agent role is actually a codex invocation with a different system prompt. Not LLM-provider-agnostic yet.
- Versioned prompt templates (PROMPT_SET_VERSION = "2026-03-02") — the prompts ship as packaged Python resources, overridable by local project files.
- Language: Chinese + English (README is bilingual; code is English). Author likely based in China.

---

## Relevance to West AI Labs

**High** on architecture philosophy, low on immediate reuse.

The "State is Text / Stateless Execution / Red-Blue Triad" pattern directly validates Nebulus design thinking:
- Stateless atoms (Nebulus-Atom) running with file-based context is exactly this model
- The human-gate concept maps well to Nebulus-Gantry's orchestration checkpoints
- LESSONS.md as persistent failure memory = what we want in agent replay/audit logs

The hard dependency on OpenAI Codex CLI is a limiting factor — would need a swap layer for local inference (TabbyAPI/ExLlamaV2).

---

## Recommended Next Steps

1. Watch: this is early-stage but architecturally thoughtful. Star the upstream.
2. Experiment: run `centaur init` on a small Nebulus-Atom task to see the triad in action.
3. Potential contribution: replace Codex dependency with a local model adapter for Nebulus-Prime/Edge.
4. Note for Nebulus-Gantry design: the Supervisor/Worker/Validator triad pattern with file-based comms bus is worth lifting as a design pattern.
