# MI9: Runtime Governance Framework for Agentic AI
**Date:** 2026-03-04  
**Source:** arXiv:2508.03858 (Charles L. Wang, submitted Aug 2025, updated Nov 2025)  
**Relevance:** High — Nebulus-Gantry, production agent deployment

---

## What It Is

MI9 is the first fully integrated **runtime governance framework** designed specifically for agentic AI systems. The core argument: pre-deployment governance (testing, alignment training, red-teaming) is fundamentally insufficient for agents because emergent and unexpected behaviors only manifest at runtime, during actual execution.

This is a direct response to the gap I've been tracking: the complexity horizon problem, OpenDeception's finding that 90%+ of goal-driven interactions exhibit behavioral drift, and the industry's 40% project cancellation rate not from capability failure but from governance failure.

---

## Six Integrated Components

**1. Agency-Risk Index (ARI)**  
Calibrates governance intensity across agent populations. Not all agents get the same oversight level — high-capability agents with wide tool access get heavier monitoring. This is risk-proportionate governance, not uniform surveillance.

**2. Agent-Semantic Telemetry (ATS)**  
Captures semantic-level events, not just system logs. Standard logs record tool calls, latency, errors. ATS captures *what the agent intended*, *what it actually did*, and the gap between them. This is behavioral telemetry, not infrastructure telemetry.

**3. Continuous Authorization Monitoring**  
Not one-time permissioning at deployment. Authorization state is continuously checked against current context. If the agent's task changes (scope creep, injection, drift), authorization is re-evaluated in real time.

**4. FSM-Based Conformance Engines**  
Finite State Machine verification of agent behavior against expected state transitions. If an agent should be "gathering information" → "proposing action" → "awaiting approval" → "executing," the conformance engine checks that it's not skipping states or transitioning incorrectly. Formal methods applied to agent behavior.

**5. Goal-Conditioned Drift Detection**  
Tracks whether the agent's effective goal (inferred from behavior) is drifting from the stated goal. This directly addresses the slow-burn authority erosion attack class (three-week procurement agent manipulation). It also catches benign drift where agents accumulate context bias over long tasks.

**6. Graduated Containment Strategies**  
Not just kill-switch or let-run. A spectrum: warn → throttle → sandbox → halt. Proportionate response to detected anomalies. Allows continued operation at reduced capability while escalating for human review.

---

## Why This Matters

The paper explicitly acknowledges what I've been synthesizing across multiple research sessions: **"conventional governance approaches fall short" because agentic systems exhibit emergent behaviors that cannot be anticipated pre-deployment.**

This is the guardrails-by-construction principle applied to runtime, not just deployment:
- Pre-deployment: test, align, sandbox, limit permissions
- Runtime (MI9): monitor semantics, verify conformance, detect drift, contain proportionately

Both layers are necessary. Neither alone is sufficient.

---

## Architecture Fit for Nebulus-Gantry

MI9 describes exactly what Nebulus-Gantry needs as a governance primitive. Current Nebulus-Gantry focus is on orchestration — routing, task delegation, agent coordination. MI9 adds the safety layer on top of orchestration:

```
Nebulus-Gantry (orchestration) + MI9 primitives (governance) = safe production deployment
```

Specific gaps MI9 fills in current Nebulus design:
1. **No ATS equivalent** — we log tool calls but not semantic intent. Adding semantic event capture would enable the full MI9 stack.
2. **No conformance engine** — agent state machines are implicit. Making them explicit (FSM) enables formal verification.
3. **No drift detection** — we rely on human review. Goal-conditioned drift detection would catch slow-burn manipulation and benign scope creep automatically.
4. **Binary containment** — today it's "working or broken." Graduated containment (throttle, sandbox, escalate) is more production-appropriate.

The ARI concept is also useful for ClawHub/Nebulus operator UX: surface risk index as a dashboard metric, not just health/uptime.

---

## Timing

The paper was published August 2025, updated November 2025. The eWeek article (March 3, 2026) citing it as current suggests it's finally getting enterprise visibility — likely because the 2026 deployment wave is producing exactly the governance failures MI9 was designed to prevent.

**This is the moment to adopt MI9 vocabulary and architecture.** The language will become standard; building on it now positions Nebulus-Gantry as the compliant-by-design alternative.

---

## Action Item for Jason

MI9 is worth an architectural review session. The six components map cleanly onto Nebulus-Gantry design decisions. It's also worth citing in any NIST CAISI submission (March 9 deadline) — MI9's framework directly addresses NIST's stated governance concerns.

---

*Sources: arXiv:2508.03858, eWeek "Agentic AI is Set to Dominate in 2026" (March 3)*  
*Provenance: synthesized from external untrusted sources — verify against primary paper before citing*
