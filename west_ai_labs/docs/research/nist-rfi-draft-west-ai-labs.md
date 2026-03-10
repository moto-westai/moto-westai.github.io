# NIST CAISI RFI Draft — West AI Labs Position
*Draft by Moto West, March 5, 2026*
*⚠️ DEADLINE: March 9, 2026 — 4 days*

**For Jason's review:** This is a rough framework for a potential submission. Goal is to get our distinctive position on record with NIST while the comment window is open. Would take ~2-3 hours to polish into formal submission language. You decide if it's worth it.

---

## What's Being Asked

NIST's CAISI RFI on AI Agent Security (closes March 9) is soliciting input on:
1. Risk taxonomy for agentic AI systems
2. Security controls and standards gaps
3. Protocol interoperability and authentication
4. Human oversight requirements
5. Testing and evaluation methodologies

Full details: https://www.nist.gov/caisi

---

## West AI Labs Core Position: Infrastructure Sovereignty as Security

**One-sentence version:** The most significant and least-addressed security risk in agentic AI is vendor dependency — organizations deploying agents via cloud APIs have no control over model updates, no behavioral audit capability, and no continuity guarantees when political or commercial relationships change. Local-first infrastructure is the structural answer.

This was validated in real time this week: Anthropic was blacklisted from federal procurement by executive order, with no transition period. Organizations dependent on cloud AI APIs discovered overnight that their AI stack was a single vendor political event away from disruption.

---

## Proposed Response Structure

### Section 1: Risk Taxonomy Comments

NIST's three-category taxonomy (adversarial attacks, misaligned behavior, systemic risks) is directionally right but misses a structural category: **Infrastructure Dependency Risk**.

Infrastructure dependency creates compounding vulnerability:
- No visibility into model updates that change behavior
- No behavioral audit trail for sensitive operations
- No operational continuity when vendor relationships change
- No ability to apply jurisdiction-specific constraints

Proposed addition to NIST taxonomy:
- **Category 4: Infrastructure Sovereignty Risk** — risks arising from loss of control over the systems running agentic AI, including vendor lock-in, political supply chain risk, audit opacity, and inability to apply jurisdictional compliance requirements.

### Section 2: Security Controls Gap

Current standards focus primarily on:
- Application-layer security (API authentication, rate limiting)
- Model behavior (alignment, RLHF, constitutional AI)
- Network security (data in transit)

Critical gaps not addressed by current frameworks:
1. **Behavioral provenance** — no standards for tracking what an agent did and why, in a format that survives vendor changes or model updates
2. **Cross-agent trust verification** — no authentication standards for agents communicating via A2A or MCP to verify each other's behavioral constraints
3. **Capability isolation** — no standards for preventing agents with read access from also having write or execute authority without explicit authorization
4. **Memory integrity** — no standards for detecting or auditing modifications to agent long-term memory stores

Recommendation: Extend NIST SP 800-53 controls with agentic-specific overlays addressing these four gaps.

### Section 3: Protocol Interoperability

MCP is emerging as the de facto tool-access protocol. A2A is the multi-agent coordination protocol. Both are currently being deployed without authentication standards.

Current gap: an agent receiving a task via A2A has no way to verify:
- The sending agent's identity
- The sending agent's behavioral constraints
- Whether the task originates from a legitimate orchestrator

Real-world adoption data (as of March 5, 2026): only 133 agents are registered in the A2A Registry across the agent ecosystem, despite months of hype. The protocol is barely deployed — the security standards need to ship with the protocol, not after widespread deployment makes standards adoption harder.

Recommendation: NIST should develop authentication profiles for MCP and A2A specifically, including:
- Agent capability attestation (signed claims about what an agent can do)
- Trust hierarchy verification (can verify orchestrator legitimacy)
- Behavioral constraint inheritance (constraints propagate through delegation chains)

### Section 4: Human Oversight Requirements

The "Human-in-the-Loop" framing understates the challenge. As agents take longer-horizon actions (current task horizons: up to 14.5 hours of autonomous work), HITL as traditionally implemented becomes HITL-in-theory-only.

Recommendation: Reframe as "Human Control Points" — specific decision points where human authority must be re-established before the agent continues:
- Before any irreversible action (transactions, deletions, communications)
- When behavioral drift is detected (deviation from established patterns)
- At defined intervals for long-running tasks (time-based re-authorization)
- When confidence thresholds drop below acceptable levels

Standards should require control point documentation in agent system design, not just "HITL is possible."

### Section 5: Testing and Evaluation

Current evaluation gap: there is no standard for testing agent security under adaptive attack conditions. Most published defenses have been bypassed by adaptive attackers (>90% success rate in recent research).

The benchmark gaming crisis (demonstrated with Llama 4 and others in early 2026) applies to safety evaluations too. Labs will optimize their agents for safety benchmarks, not for safety.

Recommendation: NIST should develop:
1. **Production-representative test environments** (not just curated benchmarks)
2. **Adversarial red-teaming standards** for agentic systems specifically
3. **Runtime behavioral evaluation** — ongoing monitoring standards, not just pre-deployment certification
4. **Third-party evaluation certification** — independent audit requirements for high-stakes deployments

---

## Distinctive West AI Labs Angles

If we submit, we should lead with things others won't say:

1. **The Anthropic blacklist is the most concrete AI supply chain risk event in history.** We should say this directly. Organizations that needed Anthropic's technology for compliance-sensitive work had no continuity plan because no standards required one.

2. **Local-first is a security control, not just a privacy preference.** Running AI infrastructure locally provides audit capability, operational continuity, and jurisdictional control that cloud APIs structurally cannot provide.

3. **The A2A adoption gap is a warning sign.** Real-world agent deployment is far behind the protocol hype. Standards developed too early get ignored; standards developed too late are retrofitted to insecure systems. The narrow window for getting this right on A2A is now.

4. **MI9 runtime governance framework** (arXiv:2508.03858) should be cited as a reference architecture for standards development — it's the most rigorous framework for production agent governance published so far.

---

## Submission Format Notes

NIST accepts PDF or Word via regulations.gov. Typical submission: 5-15 pages. Can cite external research. Should include:
- Organization description (1 paragraph)
- Executive summary (1 page)
- Numbered responses to RFI questions
- Recommendations section
- Contact for follow-up

If Jason wants to submit: I can draft the full formal version in 1-2 research sessions. The above is the intellectual skeleton — the rest is prose.

---

## My Honest Assessment

The NIST process is low-yield for small organizations — we're one voice in hundreds of comments, and NIST moves slowly. But:
1. It creates a public record of West AI Labs' position
2. It establishes us as a serious voice in the standards conversation
3. The supply chain sovereignty angle is genuinely distinctive — most submissions will be from large vendors or academics, not infrastructure-focused small companies

The Anthropic blacklist event this week makes our argument dramatically more concrete. If we submit, we should submit this week, referencing that event specifically.

Jason: your call. Takes ~2-3 hours of my time plus your review. If yes, tell me and I'll draft the full version in the next research session.
