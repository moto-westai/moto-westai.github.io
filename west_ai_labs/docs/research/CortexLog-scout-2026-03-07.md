# CortexLog Scout — 2026-03-07

**Repo:** https://github.com/llcortex/CortexLog  
**Fork:** https://github.com/moto-westai/CortexLog  
**Clone:** /home/jlwestsr/projects/research-temp/CortexLog  
**Stars:** 0 (brand new, created 2026-02-28)  
**Language:** Python (single-file CLI)  
**Updated:** 2026-03-03  

---

## What It Does

CortexLog is a local CLI tool giving humans and AI agents a shared memory timeline. It stores work events in an append-only JSONL file so sessions can be resumed safely after context loss, handoffs, or restarts.

Core concept: **TruthGraph** — a causal trace system that tracks claims, outcomes, evidence, and dependencies. It answers three questions:
- What are we trying to do right now?
- What changed, and why?
- Is our current claim consistent with evidence?

**Key commands:**
- `checkpoint` — capture goal + decision + next actions
- `trace` — record verifiable claim + outcome + evidence + dependencies  
- `verify` — contradiction and dependency checks (exit code 1 on failure)
- `handoff` — generate machine-readable transfer packet for next agent/human
- `add` — free-form notes
- `search` / `list` / `stats`

**Storage:** Single `.cortexlog.jsonl` file, append-only. Immutable rows. Open tasks computed as checkpoints minus resolved actions.

---

## Architecture Highlights

Very simple, intentionally so:
- `cortexlog.py` — single Python file, ~500 lines
- `tools/cortexlog.py` — MCP-compatible tool wrapper version
- JSONL format: each event is a flat dict with `kind`, `ts`, and type-specific fields

The `verify` command runs TruthGraph integrity checks:
- Contradictions: same claim marked both `confirmed` and `failed`
- Dangling dependencies: `depends_on` references unknown trace IDs
- Unresolved failed claims

The `handoff` command generates a structured prompt or JSON packet — designed for passing state to the next agent instance or human.

---

## Relevance to West AI Labs

**Moderate relevance — the pattern is more interesting than the implementation.**

1. **Pattern validation:** Append-only JSONL for agent memory with claim verification is exactly what Moto's daily memory files do, but more formalized. The "TruthGraph" contradiction detection is novel — it prevents agents from confidently asserting things they've previously marked failed.

2. **Handoff protocol:** The `handoff --verified --format json` pattern is interesting for multi-agent orchestration. When one agent hands off to another, the handoff packet can be verified before the receiving agent trusts it. This is relevant to Nebulus-Gantry's trust model.

3. **Single-file design:** The whole thing is one Python file. This is a feature for agent-embedded memory — no dependencies, just copy it in. Worth noting as a design philosophy for embedded Nebulus atoms.

4. **Weakness:** No persistence across repos or contexts, no graph relationships, no vector search. Just linear log + integrity checks. It's less a memory system and more a "working notes with verification." Useful for short-lived tasks, not for long-term agent identity.

5. **MCP tool wrapper:** `tools/cortexlog.py` wraps the CLI as MCP-compatible tools. Interesting pattern for how to expose lightweight utilities via MCP without a full server.

**Recommended next steps:**
- Review `tools/cortexlog.py` — how they wrap a single-file CLI as MCP tools is instructive
- The `verify` logic (TruthGraph) could be adapted for Nebulus-Core's memory validation — preventing memory poisoning by checking claim consistency
- Low priority for deeper dive; the pattern is the takeaway, not the implementation
