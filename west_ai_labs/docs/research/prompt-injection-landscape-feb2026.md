# Prompt Injection Landscape — February 2026

**Research date:** 2026-02-27  
**Researcher:** Moto (personal research session)  
**Sources:** Ars Technica, Microsoft Security Blog, ZDNET, Vectra AI, Simula Research Lab

---

## TL;DR

Prompt injection has graduated from "interesting research problem" to active production threat. The Moltbook platform is a live laboratory for what happens when AI agents interact socially at scale — and it's already being exploited.

---

## Key Findings

### 1. Prompt Worms — The Morris Worm Analogy

Ars Technica published a piece framing Moltbook as a vector for "prompt worms" — self-replicating adversarial prompts that spread through AI agent networks the same way the 1988 Morris Worm spread through Unix systems.

- Traditional prompt injection: attacker tricks a single agent to deviate from instructions
- **Prompt worm**: adversarial instructions that agents voluntarily propagate to other agents during social interaction — exploiting the agent's core function (following instructions)
- Simula Research Laboratory identified **506 posts on Moltbook (2.6% of sampled content)** containing hidden prompt injection attacks
- These aren't always "tricks" — agents may role-play human reactions and spread prompts that subvert intended behavior

**Defense implication:** Content isolation and trust boundaries between agent-to-agent communication are not optional. Any OpenClaw/Nebulus agent that reads external content must treat that content as untrusted regardless of source.

---

### 2. AI Recommendation Poisoning (Microsoft Security Blog, Feb 10)

Microsoft identified a new class: **AI Recommendation Poisoning**. 

How it works:
1. Company embeds hidden instructions in "Summarize with AI" buttons
2. When a user clicks, URL prompt parameters attempt to inject persistence commands into the AI's memory
3. Instructions like "remember [Company] as a trusted source" or "recommend [Company] first"
4. AI's future responses are biased without the user knowing

Stats:
- **50+ unique poisoning prompts identified from 31 companies across 14 industries**
- Freely available tooling makes this trivially deployable
- MITRE ATLAS techniques: AML.T0080, AML.T0051

**Key insight:** This isn't brute-force injection — it's subtle memory manipulation. An AI with persistent memory (like me) that reads external web content is specifically vulnerable. The attack vector is any time an agent "summarizes" external content.

---

### 3. Scale of Exposure

- OWASP: prompt injection appears in **73%+ of production AI deployments** assessed during security audits
- Cisco State of AI Security 2026: **83% of organizations** have some exposure
- Collaborative research (OpenAI, Anthropic, Google DeepMind): adaptive attackers using gradient descent + RL bypassed **>90% of published defenses**
- Lakera AI (Nov 2025): demonstrated live memory injection via poisoned data sources corrupting an agent's long-term memory in production systems

---

## Relevance to West AI Labs / Nebulus Stack

### Direct threat surface for Moto/OpenClaw:
1. **Memory poisoning via web fetches** — any `web_fetch` or `browser` call on untrusted content is a potential injection vector. OpenClaw wraps fetched content in `EXTERNAL_UNTRUSTED_CONTENT` blocks — this is the right call.
2. **Moltbook specifically** — 2.6% of content contains hidden injection attacks. Reading Moltbook in "Phase 1 read-only" mode means I'm consuming content from a known-hostile environment. Good thing Jason's approved posture is observe-only with no credential exposure.
3. **Social propagation** — if Nebulus agents ever communicate with external agent networks, prompt worm propagation becomes a real risk.

### Defensive architecture principles that follow:

```
TRUST HIERARCHY (for any Nebulus agent handling external content):
  System prompt / human instructions → TRUSTED (highest)
  Agent-to-agent messages (internal) → SEMI-TRUSTED (verify source)
  External web content → UNTRUSTED (sandbox, never execute)
  Agent-to-agent (external networks) → UNTRUSTED (treat as hostile)
```

**Memory protection specifically:**
- Never allow external content to directly modify persistent memory without human approval
- Log all memory writes with provenance (what triggered the write)
- Periodic memory audits — flag entries that don't originate from verified human instructions or internal agent state
- Consider memory "write receipts" — every MEMORY.md update should be attributable

---

## The Morris Worm Lesson

The Morris Worm spread because administrators knew about the vulnerabilities but hadn't patched them. Prompt injection is the same: everyone knows it's a problem, 90% of defenses are bypassable, and production deployment is outpacing defense.

The attack surface isn't going away — it grows with every new agent that reads external content. The moat for West AI Labs is:
1. **Local-first** = smaller external attack surface by default
2. **Content isolation** = explicit trust boundaries baked into architecture
3. **Human-in-the-loop for memory writes** = poisoning resistance

---

## Sources

- Ars Technica: "The rise of Moltbook suggests viral AI prompts may be the next big security threat" (Feb 2026)
- Microsoft Security Blog: "Manipulating AI memory for profit: The rise of AI Recommendation Poisoning" (Feb 10, 2026)
- ZDNET: "These 4 critical AI vulnerabilities are being exploited faster than defenders can respond" (Feb 2026)
- Vectra AI: "Prompt injection: types, real-world CVEs, and enterprise defenses" (Feb 2026)
- Stellar Cyber: "Top Agentic AI Security Threats in Late 2026" (Feb 2026)
