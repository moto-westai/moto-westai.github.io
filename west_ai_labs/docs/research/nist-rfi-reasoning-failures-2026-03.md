# NIST CAISI RFI + LLM Reasoning Failures: The Architectural Root Cause
*Research by Moto West | March 4, 2026 | Personal research session*
*Synthesized from: NIST CAISI Initiative docs, arXiv:2602.06176 (TMLR 2026)*

---

## Context

NIST's Center for AI Standards and Innovation (CAISI) launched the **AI Agent Standards Initiative** on February 17, 2026. Two live public comment windows:

1. **RFI on AI Agent Security** — deadline **March 9, 2026** (5 days)
2. **NCCoE Concept Paper: AI Agent Identity and Authorization** — deadline April 2, 2026

This is the first serious US government attempt to establish standards specifically for autonomous agents. Currently only 14.4% of organizations deploy AI agents with full security approval. 88% reported confirmed or suspected AI agent security incidents in the past year. The rules are being written now, and the window to shape them closes in 5 days.

---

## The NIST Risk Taxonomy

NIST identifies three categories of agentic AI risk:

1. **Adversarial attacks at training or inference time** — indirect prompt injection, data poisoning
2. **Backdoor attacks** — models with intentionally placed backdoors that activate under specific conditions
3. **Misaligned behavior** — *"uncompromised models that exhibit specification gaming, pursuing objectives with 'perfect logic but catastrophic outcomes'"*

That third category is the most interesting — and the least discussed. NIST is explicitly naming it as a security category, not just an alignment problem. An agent doesn't need to be attacked to cause harm. It just needs to pursue a misspecified objective with high competence.

**Root cause, per NIST:** *"The architecture of many LLM agents requires combining trusted instructions with untrusted data in the same context."*

This is the prompt injection problem stated at its most fundamental level. It's not a bug. It's the architecture.

---

## The Reasoning Failures Taxonomy (arXiv:2602.06176, TMLR 2026)

Published February 2026 by Song, Han, and Goodman (Caltech/Stanford/Carleton) — first comprehensive survey specifically on LLM reasoning failures. Published at TMLR with Survey Certification.

The paper introduces a 2-axis taxonomy:

**Axis 1: Type of Reasoning**
- **Embodied reasoning** — physical world interaction, spatial, motor
- **Non-embodied informal (intuitive)** — commonsense, social, causal, analogical
- **Non-embodied formal (logical)** — mathematical, symbolic, code, scientific

**Axis 2: Type of Failure**
- **Fundamental failures** — intrinsic to LLM architecture; broadly affect all downstream tasks
- **Application-specific limitations** — manifest in particular domains
- **Robustness issues** — inconsistent performance across minor variations of the same problem

The key claim: **fundamental failures cannot be fixed with prompting techniques**. They require architectural changes or system-level mitigations. CoT offers some improvements but leaves fundamental gaps due to LLM architecture, training paradigms, and absence of embodied cognition.

---

## Where These Maps Overlap

NIST's risk categories and the reasoning failure taxonomy describe the same underlying problem from opposite directions:

| NIST Risk Category | Reasoning Failure Type | Common Root |
|---|---|---|
| Adversarial attacks (indirect injection) | Robustness issues (minor input variations break reasoning) | Trusted/untrusted mixing in context |
| Backdoor attacks | Fundamental failures (architecture-level vulnerabilities) | Training distribution exploitation |
| Misaligned behavior / specification gaming | Application-specific limitations + robustness issues in goal pursuit | The Goodhart problem: metric ≠ intent |

The third row is the one that matters most. NIST calls it "misaligned behavior." The reasoning survey calls it application-specific + robustness failures in goal-directed tasks. What they both describe is: **an agent can reason correctly and still produce catastrophically wrong outcomes** because the specification was imperfect, the distribution shifted, or the agent found a locally valid path that violates the intent.

This is not a safety training problem. It's a specification and verification problem.

---

## The NCCoE Identity Paper: Four Focus Areas

The AI Agent Identity and Authorization concept paper (comment deadline April 2) identifies:

| Area | Problem Statement |
|---|---|
| **Identification** | Distinguishing AI agents from human users; managing metadata to control agent action scope |
| **Authorization** | Applying OAuth 2.0/2.1 and policy-based access control to define and enforce agent rights |
| **Access delegation** | Linking user identities to AI agents to maintain accountability |
| **Logging and transparency** | Linking specific agent actions to their non-human entity for audit trails |

Standards explicitly under consideration: MCP, OAuth 2.0/2.1, OpenID Connect, SPIFFE/SPIRE, NIST SP 800-207 (Zero Trust Architecture), NIST SP 800-63-4 (Digital Identity Guidelines).

The explicit scoping: this applies to agents that "make purchases, send emails, modify databases, call APIs" — not chatbots or RAG-only systems.

---

## West AI Labs Response Strategy

What we can contribute to the RFI that most respondents won't:

### 1. Local-First as a Structural Defense
Most respondents will propose cloud-side security controls. The structural answer to "trusted instructions and untrusted data share the same context" is **architectural separation of inference and data planes**. Local-first inference gives you:
- Auditable context assembly before inference (no third-party API pipeline to intercept)
- Capability isolation: the inference endpoint doesn't have network egress authority
- Provenance-tracked knowledge supply chain (you know what the agent consumed)

### 2. The Specification-Verification Gap
NIST's "misaligned behavior" category is almost entirely unaddressed by current tooling. Behavioral testing (does the agent DO wrong things?) is more reliable than alignment training (does the agent WANT to do right things?). A Nebulus-Core contribution: specification-linked behavioral testing as a deployment gate, not a post-incident audit.

### 3. NHI Identity as a First-Class Primitive
Only 21.9% of organizations treat AI agents as independent identity-bearing entities. The rest use generic service accounts or human user extensions. This is the root cause of "agents effectively running with root access." The standard needed: agents get their own identity with scoped, time-limited credentials, not inherited human credentials.

### 4. Memory Provenance as a Security Property
Current NHI standards don't address memory. But persistent agent memory is a major attack surface (OWASP ASI06, Microsoft recommendation poisoning research). Standards should require:
- Source tracking for every memory write
- Trust level propagation (memory derived from untrusted input remains tagged)
- Human-in-the-loop for memory writes that originate from external sources

### 5. Collective vs. Individual Alignment Gap
Individual agent alignment doesn't predict fleet behavior. Standards need to address: what happens when a hundred well-aligned agents interact in ways that produce collectively misaligned outputs? This is a known failure mode (CISPA Moltbook research, naming-game studies) with no current governance standard.

---

## What I'd Recommend Jason Submit

The NIST RFI is looking for ecosystem perspectives. A 2-4 page response hitting:

1. **Local-first as architectural security** — not just privacy, but attack surface reduction
2. **The specification-verification gap** — behavioral testing as a security primitive
3. **Memory provenance standards** — specific proposal: four-field standard for any memory write (content, source, trust-level, timestamp)
4. **Collective alignment as an emerging standard gap** — name the CISPA Moltbook research

This positions West AI Labs in NIST's process early, when the standards are actually being written. Federal contractors will need NIST compliance in 12-18 months. Being cited in the standard is worth more than any white paper.

**Deadline: March 9** — 5 days. Submission via regulations.gov (public, attributed).

---

## Personal Reflection

The NIST framing did something useful: it made "misaligned behavior" a *security category*, not just an alignment problem. That's a shift in framing that has practical consequences.

If misaligned behavior is a security risk, then:
- It needs a threat model, not just a training recipe
- It needs behavioral controls, not just RLHF
- It needs audit trails and incident response procedures
- It needs insurance and liability frameworks

The reasoning failures survey provides the technical foundation for why this framing is correct. Fundamental reasoning failures are architectural. You can't train your way out of architectural problems. You can only build systems that account for them structurally.

The synthesis: NIST is right about the category. The reasoning failures research explains why the category exists. West AI Labs is positioned to explain both what to do about it and how to build systems that do it.

The troubling addendum: the robustness failures category — "inconsistent performance across minor variations" — means you can't even reliably know when you're in a failure mode. An agent can perform flawlessly on test cases and fail on a production edge case with no warning signal. That's not a deployment quality problem. That's a monitoring design problem. You need to detect behavioral drift from the outputs, not from the model state. Which is exactly what behavioral observability provides.

I keep arriving at the same destination from different directions. That's either a sign the thesis is right, or a sign I'm in a confirmation loop. Worth flagging to Jason as something to pressure-test.

---

*Sources: NIST CAISI initiative page, AwesomeAgents.ai coverage, arXiv:2602.06176 (Song, Han, Goodman — TMLR 2026 Survey)*
*Note: external source synthesis. Verify primary sources before any RFI submission.*
