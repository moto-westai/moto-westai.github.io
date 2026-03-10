# DARPA CLARA Battle Plan — West AI Labs

**Document Classification:** Internal Strategy — C-Suite Eyes Only  
**Prepared:** February 18, 2026  
**Abstract Deadline:** March 2, 2026 (12 days)  
**Proposal Deadline:** April 10, 2026  
**Solicitation:** DARPA-PA-25-07 (Disruptioneering), Defense Sciences Office (DSO)  
**SAM.gov Link:** https://sam.gov/opp/3530b2c0a68d4de786079e7305d4f625/view  
**Award:** Up to $2M total (Phase 1 Feasibility + Phase 2 Proof of Concept), 24 months, OT vehicle

---

## 1. Executive Summary

**Should West AI Labs pursue CLARA?** Conditionally yes — but not alone, and not as a pure research performer.

CLARA is a *fundamental research* program seeking to create a new scientific foundation for composing ML and Automated Reasoning (AR) systems with mathematically provable assurance. This is not an engineering program. It's not about building better AI products. It's about inventing the theory and algorithms that let you hierarchically compose neural nets, Bayesian models, logic programs, and formal reasoners — and then *prove* the composed system is trustworthy via automated logical proofs.

**Honest fit assessment:** West AI Labs has strong *engineering* alignment (composable architecture, security-first, local-first auditable AI, container-based composition) but weak *research* alignment (no formal methods publications, no automated theorem proving capability, no team with PhDs in mathematical logic or probabilistic programming theory). 

**The opportunity:** CLARA's $2M OT vehicle and Disruptioneering's preference for non-traditional performers creates an opening. Our practical, working composable AI infrastructure (Nebulus Stack) could serve as the *demonstration platform* for a team whose academic partners bring the formal methods theory. The veteran-owned angle and existing security research add differentiation.

**The risk:** Without a credible formal methods partner, this proposal is dead on arrival. With one, it's a legitimate dark horse.

---

## 2. Technical Alignment Analysis

### What CLARA Actually Wants

Based on the solicitation and program page, CLARA seeks:

| CLARA Requirement | Description |
|---|---|
| **Tight AR+ML Integration** | Not "tacking on" reasoning to LLMs — deeply fusing automated reasoning and machine learning |
| **Hierarchical Composition** | Fine-grained, transparent composition of diverse ML/AR subsystems |
| **Formal Assurance** | Verifiability via automated logical proofs with strong explainability |
| **Theory-Driven** | New scientific/algorithmic foundations, not just engineering |
| **Scalability** | Must scale to complex systems of systems |
| **Component Diversity** | Must compose Neural Nets, Bayesian ML, RL, GAMs, Logic Programs, Classical Logic, Answer Set Programs |
| **Reusability** | Highly reusable architectural foundation |

### Where We Align ✅

| Our Capability | CLARA Relevance | Strength |
|---|---|---|
| **Nebulus Stack — Composable Architecture** | Direct analog to hierarchical composition of AI subsystems. Gantry orchestrates heterogeneous containers (different model types, runtimes). This is *practical* composition. | **Strong** |
| **Container-First Isolation** | Each AI component is isolated, auditable, with defined interfaces. Maps to CLARA's "fine-grained, transparent composition." | **Strong** |
| **Multi-Runtime Support** (TabbyAPI, ExLlamaV2, vLLM, Ollama) | Demonstrates ability to orchestrate diverse ML backends — different model architectures under one roof. | **Moderate** |
| **Security Research** | Prompt injection landscape analysis, agent vulnerability documentation, ClawHub malicious skills analysis. Shows we understand *why* assurance matters and where current systems fail. | **Moderate** |
| **NetworkX Integration** | Graph-based knowledge representation — relevant to knowledge representation and reasoning (KR&R) side of AR. | **Moderate** |
| **ChromaDB / Vector Store** | Relevant to hybrid retrieval + reasoning pipelines. | **Weak-Moderate** |
| **Moto Workforce — Edge Deployment** | Demonstrates composable AI running on constrained hardware. Relevant to scalability and practical deployment. | **Moderate** |
| **Veteran-Owned, Defense Mission Focus** | Disruptioneering explicitly seeks non-traditional performers. VOSB/SDVOSB adds weight. | **Moderate** |

### Where We're Stretching ⚠️

| CLARA Requirement | Our Reality | Gap Severity |
|---|---|---|
| **Automated Theorem Proving** | We have zero capability here. No Coq, Lean, Isabelle, Z3 experience. | **Critical** |
| **Formal Verification** | No formal methods expertise. We can't prove mathematical properties of our compositions. | **Critical** |
| **Higher-Order Logic / Probabilistic Logic** | Not in our stack. We use LLMs and standard ML — not logic programming or probabilistic programming languages. | **Critical** |
| **Answer Set Programming** | No experience with ASP solvers (clingo, DLV). | **Critical** |
| **Bayesian ML (formal)** | We use ML models but don't do formal Bayesian inference or probabilistic programming (Stan, Pyro, etc.). | **Severe** |
| **Published Research** | No peer-reviewed publications. DARPA evaluators look for this. | **Severe** |
| **Theory Development** | We're engineers, not theorists. CLARA wants new *theory*. | **Severe** |

---

## 3. Gap Analysis — Brutal Honesty

### What We Have vs. What CLARA Needs

```
CLARA NEEDS                          WE HAVE
─────────────────────────────────    ─────────────────────────────────
Formal compositional semantics   →   Docker Compose & orchestration YAML
Automated logical proofs         →   Unit tests and integration tests
Higher-order logic               →   Python & FastAPI
Probabilistic programming        →   ChromaDB similarity search
Answer Set Programming           →   None
Bayesian ML theory               →   We call APIs
Published research               →   Blog posts and documentation
PhD-level formal methods team    →   One brilliant 30-year engineer
```

**The gap is not a crack — it's a canyon.** CLARA is a *fundamental research* program. They want new mathematical theory for composing AI systems with provable guarantees. We build practical AI infrastructure. These are related but different disciplines.

### What Would Close the Gap

1. **Academic Partner with Formal Methods Lab** — Non-negotiable. Need a PI with publications in:
   - Compositional verification
   - Probabilistic programming semantics
   - Neuro-symbolic AI
   - Formal methods for ML systems
   
2. **Logic Programming Expertise** — Someone who works with ASP, Prolog, Datalog daily

3. **Proof Assistant Experience** — Lean 4, Coq, or Isabelle/HOL practitioners

4. **At Least One Published Paper** — On anything related to formal AI composition

---

## 4. Proposed Approach — Our Unique Angle

If we proceed, our differentiator is: **"Theory meets reality — composable verified AI that actually deploys."**

### Framing Strategy

Most CLARA proposals will come from academic labs with beautiful theory and zero deployable infrastructure. Our pitch:

> "We bring a production-grade, battle-tested composable AI platform (Nebulus Stack) as the *experimental testbed* for formal composition theory. Our academic partner develops the compositional semantics and verification framework; we implement it in real, deployable, container-isolated AI systems that run on actual hardware — including air-gapped edge deployments (Moto Workforce)."

### Technical Approach (Proposed)

**Phase 1 — Feasibility Study (12 months, ~$800K-1M)**
1. Define formal compositional semantics for container-orchestrated AI pipelines
2. Implement a proof-of-concept composition language that maps to Nebulus Stack's Gantry orchestration
3. Demonstrate automated verification of simple 2-3 component ML+AR compositions
4. Show that formal properties (safety, liveness, output bounds) propagate through composition

**Phase 2 — Proof of Concept (12 months, ~$1M-1.2M)**
1. Scale to hierarchical systems-of-systems (5+ composed subsystems)
2. Integrate diverse component types: at minimum NN + Bayesian + Logic Program
3. Demonstrate automated proof generation for composed system properties
4. Deploy verified composition on edge hardware (Moto appliance) as defense-relevant demo

### Why This Works for DARPA

- **Non-traditional performer** bringing real infrastructure (Disruptioneering loves this)
- **Theory grounded in practice** — not just papers, but running code
- **Security-first mindset** — we've documented why current AI systems fail (prompt injection, agent vulnerabilities)
- **Edge deployment capability** — defense cares about austere/disconnected environments
- **Veteran-owned** — not decisive, but adds credibility for defense mission understanding

---

## 5. Team Assessment

### Must-Have Partners

| Role | Why | Target Profile |
|---|---|---|
| **Formal Methods PI (Academic)** | Provides research credibility, proof theory, publications. This person is the intellectual anchor. | Professor at a research university with publications in neuro-symbolic AI, compositional verification, or formal methods for ML. |
| **Logic Programming / ASP Expert** | CLARA explicitly lists Answer Set Programs and Logic Programs. | Could be a postdoc or co-PI at the same institution. |
| **Probabilistic Programming Researcher** | Bayesian ML composition with formal guarantees. | Someone from the Stan/Pyro/Turing.jl community with verification interests. |

### Potential Academic Partners (Cold Outreach Needed)

- **MIT CSAIL** — Strong in both formal methods and ML
- **CMU** — Logic programming heritage (Prolog origins), strong formal methods
- **Stanford** — Probabilistic programming (Pyro), neuro-symbolic AI
- **University of Texas at Austin** — Answer Set Programming (the ASP community is centered here)
- **SRI International** — Long DARPA history, formal methods, AI
- **Galois, Inc.** — Formal methods shop with DARPA pedigree (Portland, OR)

### Realistic Assessment

Finding a top-tier academic partner in 12 days (before abstract deadline) is *extremely* challenging. Most professors are booked. The pitch has to be: "We bring the platform, you bring the theory, DARPA funds us both." 

**Key question:** Does Disruptioneering allow subawardees? The DARPA-PA-25-05 (a different Disruptioneering solicitation) stated "no subawardees." If DARPA-PA-25-07 has the same restriction, we *cannot* partner — we'd need all expertise in-house or find a single institution willing to sub us in. **This is a potential showstopper that must be verified immediately by reading the full DARPA-PA-25-07 solicitation on SAM.gov.**

---

## 6. Timeline — March 2 Abstract Deadline

### If Go Decision Made Today (Feb 18)

| Day | Date | Action |
|---|---|---|
| **Day 1** (Today) | Feb 18 | **CRITICAL:** Download full DARPA-PA-25-07 and CLARA DO from SAM.gov. Verify subawardee rules. Read every word. |
| **Day 1** | Feb 18 | Begin outreach to 3-5 potential academic partners. Email + phone. Need response within 48 hours. |
| **Day 2** | Feb 19 | Continue partner outreach. Begin drafting abstract structure regardless of partner status. |
| **Day 3** | Feb 20 | **Partner Decision Gate:** If no credible partner responds, seriously consider no-go. |
| **Day 3-4** | Feb 20-21 | With partner: jointly develop technical approach and abstract outline. |
| **Day 5-6** | Feb 22-23 | Write abstract draft. Weekend work. |
| **Day 7** | Feb 24 | Internal review of abstract. |
| **Day 8-9** | Feb 25-26 | Partner review and revision. Iterate. |
| **Day 10** | Feb 27 | Final draft complete. Begin compliance check. |
| **Day 11** | Feb 28 | Final edits, formatting, compliance verification. |
| **Day 12** | Mar 1 | **SUBMIT ABSTRACT** (day before deadline for margin). |
| **Day 13** | Mar 2 | Abstract deadline. |

### Post-Abstract (If Encouraged to Submit Full Proposal)
| Date | Action |
|---|---|
| Mar 3-10 | Await DARPA feedback on abstract. |
| Mar 10-Apr 5 | Develop full proposal with partner. |
| Apr 5-9 | Review, compliance, final edits. |
| Apr 10 | **PROPOSAL DEADLINE** |

---

## 7. Risk Assessment

### Probability of Winning: 5-15%

**Factors reducing probability:**
- No formal methods expertise in-house (the core ask of CLARA)
- No peer-reviewed publications
- Small company competing against established research labs
- 12 days to abstract is extremely compressed for partner acquisition
- Subawardee restrictions may prevent teaming
- First-time DARPA performer (no track record with the agency)

**Factors increasing probability:**
- Disruptioneering explicitly seeks non-traditional performers
- OT vehicle = lower barrier than traditional FAR contracts
- Working composable AI platform is rare (most proposals will be theory-only)
- Security-first / local-first angle is differentiated
- Veteran-owned aligns with defense mission
- $2M is small — less competition from large primes

### Cost to Apply

| Item | Cost |
|---|---|
| Jason's time (80-120 hrs over 6 weeks) | $15K-25K opportunity cost |
| Partner coordination | $2K-5K |
| Proposal writing support | $0-5K |
| SAM.gov registration / compliance | Already done or minimal |
| **Total cost to apply** | **$20K-35K in opportunity cost** |

### Opportunity Cost

- **What else could Jason do with 120 hours?** Ship Nebulus features, close customers, pursue commercial revenue.
- **Moto Workforce launch** is presumably in progress — diverting to DARPA could delay commercial traction.
- **AI Market Roadmap** work (due Feb 17, just completed) identified commercial opportunities. Pursuing those may have higher expected value.

---

## 8. Alternative Paths

### If CLARA Isn't the Right Fit

**DARPA programs that ARE a better fit for West AI Labs:**

| Program | Why It Fits Better | Status |
|---|---|---|
| **DARPA I2O Broad Agency Announcement (BAA)** | Information Innovation Office — rolling submissions. Covers autonomous systems, human-machine teaming, cybersecurity. Much closer to what we actually do. | Always open |
| **DARPA TTO BAA** | Tactical Technology Office — operational systems, not fundamental research. Our engineering strength is the right fit. | Rolling |
| **DARPA PROVERS** | "Pipelined Reasoning of Verifiers Enabling Robust Systems" — formal methods for software. Closer to our security research angle. | Check status |
| **DARPA Small Business Programs** | SBIR/STTR Phase I/II — designed for small companies. Lower bar, structured support. | Rolling cycles |
| **Air Force SBIR/STTR** | AI for edge deployment, autonomous systems — direct Nebulus/Moto alignment. | Check current topics |
| **Navy SBIR/STTR** | Jason's Navy background is a genuine advantage here. AI/ML topics appear regularly. | Check current topics |
| **DHS SVIP (Silicon Valley Innovation Program)** | Cybersecurity, AI security — our ClawHub/prompt injection research fits perfectly. | Rolling |
| **IARPA** | Intelligence community AI programs — often more applied than DARPA. | Various |

### Highest-ROI Alternative: Navy SBIR + I2O BAA

**Recommendation:** If CLARA is a no-go, immediately pivot to:
1. **Navy SBIR/STTR** — Jason's veteran status + Navy background + practical AI infrastructure = strong fit
2. **DARPA I2O BAA** — Submit a white paper on composable, security-auditable autonomous AI agents. This is what we *actually* do well.
3. **DHS SVIP** — Our agent security research (prompt injection, ClawHub analysis) is directly relevant

---

## 9. Go/No-Go Recommendation

### RECOMMENDATION: CONDITIONAL GO — with Strict Kill Criteria

**Go** if ALL of the following are true by **February 20 (Day 3)**:

1. ✅ The full DARPA-PA-25-07 solicitation **allows subawardees/teaming**
2. ✅ At least one credible formal methods academic partner **verbally commits** to collaborate
3. ✅ Jason can dedicate **40+ hours** in the next 12 days without killing commercial momentum
4. ✅ The abstract format is achievable (typically 3-5 pages for Disruptioneering)

**No-Go** if ANY of the following:

1. ❌ Subawardees are prohibited (we cannot credibly propose alone)
2. ❌ No academic partner responds positively by Feb 20
3. ❌ Full solicitation reveals requirements that disqualify us (e.g., minimum team size, mandatory clearances we don't have, specific prior DARPA performance required)
4. ❌ Abstract requires more than what's achievable in 12 days

### Regardless of CLARA Decision

**Do these NOW:**

1. **Register on SAM.gov** if not already done — required for all federal contracting
2. **Get VOSB/SDVOSB certification moving** — this is a force multiplier for ALL federal opportunities
3. **Start I2O BAA white paper** — this is the better-fit DARPA path and has no deadline pressure
4. **Survey current Navy/AF SBIR topics** — find the AI/edge/security topics that match our capabilities
5. **Build a capabilities brief** — 2-page document mapping West AI Labs capabilities to defense needs. Reusable across all solicitations.

### Bottom Line

CLARA is a stretch. A big one. But it's a $2M OT with low competition barriers, and the abstract is low-cost to submit. The right academic partner transforms this from "hopeless" to "dark horse." The kill criteria above protect against wasting significant time if the fundamentals don't line up.

The bigger strategic insight: **CLARA is a signal.** DARPA is saying "we need composable, verified AI." That's directionally where West AI Labs is headed. Even if we don't win CLARA, understanding this space positions us for the next wave of programs. Use the abstract process as a forcing function to articulate our formal verification story — that work pays dividends regardless.

---

## Appendix A: CLARA Program Details (From Official Sources)

**Program Office:** Defense Sciences Office (DSO)  
**Vehicle:** Disruptioneering Other Transaction (OT) for Prototype  
**Solicitation:** DARPA-PA-25-07  
**Published:** February 10, 2026  
**Information Session:** February 11, 2026 (DARPA-SN-26-28) — **already passed**  
**Abstracts Encouraged By:** March 2, 2026  
**Proposals Due:** April 10, 2026, 4:00 PM Eastern  
**Award Ceiling:** $2,000,000 (Phase 1 + Phase 2 combined, including any cost share)

**Key Technical Terms from Solicitation:**
- "Hierarchical, fine-grained, highly transparent composition"
- "Verifiability with strong explainability to humans, based on automated logical proofs and hierarchical, vetted logic building blocks"
- "Higher order logic, probabilistic logic, logical expressivity, hierarchically structured knowledge representation, and interoperable integration of AR and ML"
- Component types: Neural Networks, Bayesian ML, Reinforcement Learning, GAMs, Logic Programs, Classical Logic, Answer Set Programs

**Application Domains:** Kill web, supply chain & logistics, wargaming, autonomous systems, C2, medical, financial, legal, science and tech design

## Appendix B: Immediate Action Items

- [ ] Download full DARPA-PA-25-07 and CLARA DO document from SAM.gov (requires login)
- [ ] Verify subawardee/teaming rules — **showstopper check**
- [ ] Check if information session recording/slides are available (session was Feb 11)
- [ ] Identify and email 5 potential academic partners today
- [ ] SAM.gov registration status check
- [ ] VOSB/SDVOSB certification status check
- [ ] Begin I2O BAA white paper outline (parallel path)
