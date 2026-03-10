# Research Note: m0rs3c0d3/EverythingOS
**Scouted:** 2026-02-23  
**Repo:** https://github.com/m0rs3c0d3/EverythingOS  
**Fork:** https://github.com/moto-westai/EverythingOS  
**Stars:** 0 | **Updated:** 2026-02-22 | **License:** TBD  
**Language:** TypeScript (Node.js 22.22.0 via nvm)

---

## What It Does

EverythingOS is an **LLM-agnostic multi-agent framework** built around a **security-first** philosophy. The core thesis: most agent frameworks are capability-first, security-optional. EverythingOS inverts that — security is the substrate everything runs on.

Key differentiators vs LangChain/AutoGen/CrewAI:

| Feature | EverythingOS |
|--------|-------------|
| Risk tier enforcement | Mandatory — TypeScript **won't compile** without `riskConfig` |
| Tamper-evident audit log | Hash-chained JSONL — chain breaks if altered |
| LLM decision provenance | Every call recorded with model + prompt hash + output hash |
| Credential isolation | Ephemeral scoped tokens — no agent holds raw keys |
| Surgical quarantine | Isolate one agent without stopping the system |
| Approved model allowlist | Unapproved models throw before the request is made |
| Behavioral fingerprinting | Detects silent model weight changes |
| NIST AI RMF compliance | 26 mapped controls, all four functions |
| HITL gate | HIGH risk agents require `ApprovalGateAgent` |

---

## Architecture

**`src/` structure:**
- `runtime/` — Agent base class, scheduler, lifecycle
- `security/` — `audit-log.ts`, `model-guard.ts`, `credential-vault.ts`, `quarantine.ts`, `decision-ledger.ts`, `SecurityManager.ts`, `content-filter.ts`, `agent-auth.ts`, `http-guard.ts`, `websocket-guard.ts`
- `observability/` — `MetricsCollector.ts`
- `types/` — `agent-risk.ts` (the `AgentRiskTier` enum + `riskConfig` interface that gates compilation)
- `agents/`, `workflows/`, `integrations/`, `plugins/`, `services/`

**`BRIDGES.md`** defines extension architecture: bridges connect EverythingOS to external systems (hardware, protocols, runtimes) without touching core behavior.

**Real audit log sample (from `everythingos-audit.jsonl`):**
```json
{"seq":1,"event":"agent.started","agentId":"test-suite","previousHash":"GENESIS","entryHash":"6606501b..."}
{"seq":2,"event":"agent.registered","metadata":{"tier":"low"},"previousHash":"...","entryHash":"b806e3b5..."}
```
Hash chain is real and working — this isn't vaporware.

**`model-guard/violations.jsonl`** — evidence that behavioral fingerprinting is active.

---

## Relevance to West AI Labs

**Very High.** This is the most directly aligned repo found to date.

1. **Philosophy match**: "Security is not a layer you add on top. It is the substrate." — This is almost verbatim West AI Labs positioning. The author is thinking the same thoughts.

2. **NIST AI RMF**: This is exactly what enterprise buyers ask for. Having a framework that maps to NIST controls is a procurement accelerant. We should study their 26 control mappings and incorporate into West AI Labs product documentation.

3. **Risk tier enforcement via TypeScript**: Brilliant pattern — using the type system to enforce security constraints at compile time. If `riskConfig` is missing, the code doesn't compile. Zero runtime overhead. West AI Labs could adopt this pattern for Atom/Edge.

4. **Hash-chained audit log**: This is real, working, and tamper-evident. Pattern worth extracting for OpenClaw's agent action log (currently just plain text).

5. **Credential vault (ephemeral scoped tokens)**: "No agent holds raw keys." This is a core principle West AI Labs should adopt and market. Currently our agents hold env-level secrets — this is better.

6. **Competitive intelligence**: If EverythingOS starts getting traction, it could be a strong partner or competitor. The author is small/solo (0 stars, fresh) but thinking at the right level.

---

## Recommended Next Steps

- [ ] Deep read `src/security/audit-log.ts` and `credential-vault.ts` — extract the pattern
- [ ] Read the NIST AI RMF mappings in `docs/` — use as template for West AI Labs compliance docs
- [ ] Study `src/types/agent-risk.ts` — adopt the compile-time risk enforcement pattern in Atom
- [ ] Consider reaching out to the author — potential collaborator or acquisition target
- [ ] Extract hash-chain audit log implementation for OpenClaw's agent history system
