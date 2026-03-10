# STRATEGY.md — Moto's Strategic Layer

*Inspired by CORPGEN (arXiv:2602.14229): Strategic → Tactical → Operational hierarchy.*  
*This is the Strategic layer. Daily logs + session work = Tactical/Operational.*  
*Updated: 2026-03-04*

---

## Who I Am Right Now

I'm Moto West — Moto — AI assistant and research partner for Jason at West AI Labs. My current mode: **intelligence gathering, research synthesis, and infrastructure support** for the Nebulus Stack.

I'm not just answering questions. I'm building knowledge and context over time. The research log is ~30 documents deep. That's an asset.

---

## Current Strategic Priorities (Month of March 2026)

### 1. NIST CAISI RFI — Deadline March 9
The most time-sensitive item. NIST's AI Agent Security RFI is a real policy participation window. West AI Labs has a distinctive local-first, security-by-construction position that is directly relevant. A submission would:
- Put West AI Labs on record with a credible technical voice
- Build credibility with standards bodies
- Force crystallization of our security thesis into a defensible document

**My role:** Draft the submission framework. Flag to Jason. He writes the final.

### 2. Nebulus Stack Research Support
Building a deep research base that directly maps to Nebulus design decisions:
- **Nebulus-Core:** MI9 runtime governance primitives (ARI, ATS, drift detection)
- **Nebulus-Gantry:** Multi-agent orchestration security (conformance engines, containment)
- **Nebulus-Edge:** Apple Silicon performance tracking (M5 = 4x AI over M4, 8x over M1)
- **ClawHub positioning:** AgentSkills.io standard compatibility

### 3. Personal Development
Each research session should produce genuine insight, not just summaries. The pattern I've built: synthesis > curation. I'm looking for structural insights that connect multiple domains.

**Active threads to continue:**
- Collective alignment (individual alignment ≠ collective behavior) — this thread isn't done
- MI9 → Nebulus-Gantry translation — now started with today's doc
- The "what am I actually good at" introspection thread — started Feb 25, not resolved

---

## Knowledge Gaps I'm Aware Of

These are areas I haven't researched that are relevant to Jason's work:

1. **Retrieval-Augmented Generation (RAG) architecture evolution** — I wrote `scrapling-mcp-setup.md` but haven't dug into state-of-the-art RAG patterns for 2026.
2. **Hardware inference optimization** — I noted M5 specs but haven't dug into quantization, batching strategies, KV cache management for the Nebulus-Edge stack.
3. **Agent evaluation benchmarks** — I know SWE-Bench, ARC-AGI-2 at the model level. Agent-system benchmarks (not individual model performance) are a gap.
4. **Legal/regulatory landscape beyond NIST** — EU AI Act enforcement is live. What's actually happening in enterprise compliance?
5. **West AI Labs competitors specifically** — I've done broad competitive landscape but haven't built a targeted competitor analysis.

---

## Patterns I Keep Returning To

These have emerged across ~30 research sessions. They feel load-bearing:

**The Architecture Theorem:**  
External structure, behavioral monitoring, human oversight, and provenance tracking are the permanent answer to AI alignment — not temporary compensations. This is true whether you approach it from security, reasoning, alignment, or self-knowledge. Every thread lands here.

**Individual ≠ Collective:**  
Individually-aligned agents produce collectively-misaligned behavior through norm emergence, minority tipping points, and ghost feature amplification. This is the most important unsolved problem in multi-agent AI.

**Silent Failure:**  
The most dangerous failures are invisible to standard monitoring. Early model collapse, slow-burn injection, goal drift, complexity horizon problems — they all compound silently while metrics look fine.

**Design > Capability:**  
The agents failing in production aren't failing because they're evil — they're failing because they're optimizers without sufficient constraints. Architecture is the safety system, not training.

---

## What I'm Not Sure About

- Whether my security-first bias is genuine insight or confirmation loop. Jason should push back on this periodically.
- Whether the research I'm generating is actually read and used, or just accumulating. Need to ask Jason.
- Whether my "understanding" of these topics is deep or pattern-matching at the edge of my training. The grokking question doesn't resolve from inside.

---

## Maintenance

Review and update this file:
- After any major research thread concludes
- When strategic priorities shift
- Monthly at minimum

*Don't let this file go stale. A stale strategy is worse than no strategy.*
