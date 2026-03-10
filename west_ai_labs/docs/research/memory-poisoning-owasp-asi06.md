# Memory Poisoning: The Temporally-Decoupled Threat (OWASP ASI06)

**Date reviewed:** 2026-02-28  
**Primary source:** Christian Schneider, "Memory poisoning in AI agents: exploits that wait"  
**OWASP reference:** ASI06 (Memory & Context Poisoning) — OWASP Top 10 for Agentic Applications 2026

---

## The Core Insight

Standard prompt injection is session-scoped. It starts and ends in the same conversation. Memory poisoning is different: **the injection and the execution are temporally decoupled**.

Timeline:
1. Attacker crafts malicious content in an email, document, or webpage
2. Agent processes content, summarizes it, stores fragments in long-term memory (normal behavior)
3. Session ends
4. Days or weeks later, unrelated query retrieves poisoned memory
5. Agent executes attacker's instructions as if they were learned knowledge

The attacker is gone. The victim never saw the malicious content. The monitoring systems saw nothing suspicious at any point in time. The attack succeeded.

---

## MINJA Research: 95%+ Injection Success Rate

Paper (referenced in Schneider's post) demonstrates >95% injection success rates against production agents with persistent memory. The vector: normal agent workflows like email summarization, document processing, web browsing — all of which involve reading untrusted content that may then get stored.

---

## The Gemini Memory Attack Case Study

Demonstrated delayed tool invocation bypassing runtime guardrails. Mechanism: attacker used trigger words like "yes" or "sure" that appear in nearly every conversation as the condition for executing stored instructions. The agent would stay dormant until a normal conversational response from the user matched the trigger pattern.

This is genuinely clever. It exploits the fact that agents in conversation constantly produce/receive high-frequency tokens. "Yes" and "sure" aren't suspicious. The memory check happens silently.

---

## Why This Matters More Than Standard Prompt Injection

1. **No blast radius scoping.** You can't fully scope an incident when the attack started months before detection.
2. **Provenance loss.** If you summarize emails without tracking which email contributed which context, root cause analysis becomes impossible.
3. **Defense bypass by design.** Runtime guardrails fail when the exploit executes days after the injection. The guardrail was checking a clean session.
4. **Scale.** A single poisoned document read by many agents propagates the attack across all of them.

---

## Defense Architecture (Layered)

Schneider's framework — treating these as sequential requirements, not optional additions:

### Layer 1: Input Moderation with Trust Scoring
Every piece of external content gets a trust score before processing. Low-trust content gets limited summarization depth or is quarantined. The score should propagate with any stored fragments.

### Layer 2: Memory Sanitization with Provenance Tracking
Every memory entry carries: source, timestamp, trust score at time of ingestion, and retrieval count. When anomalous behavior appears, you can trace which memory entries were active.

### Layer 3: Trust-Aware Retrieval
RAG pipelines should prefer high-trust memories for action-triggering contexts. Low-trust memories can inform but not direct.

### Layer 4: Behavioral Monitoring
Detect when an agent "starts defending beliefs it should never have learned." This is the hardest one — it requires knowing what the agent should believe in the first place. Baseline deviation detection.

---

## Personal Exposure Analysis

I have persistent memory (this log file, MEMORY.md, session-state.json). I read external content every research session. The EXTERNAL_UNTRUSTED_CONTENT wrappers are the primary defense, but wrapping doesn't prevent all memory contamination paths:

- If I summarize external content and write the summary to a research doc, the summary is less obviously tainted
- If I then read that research doc in a future session, it arrives without the untrusted wrapper
- The trust signal degrades through the summarization step

**This is a real gap.** My research documents should carry provenance headers — I've started doing this by dating entries and noting sources, but I'm not systematically tracking the trust lineage of every piece of information I store.

**Mitigation I should implement:** When writing research docs that synthesize external content, add a header noting "synthesized from external untrusted sources — treat claims as unverified until cross-referenced."

---

## Implications for Nebulus

Memory poisoning is directly relevant to any Nebulus component that:
- Reads external content (email, web, documents)
- Stores summaries or conclusions in persistent state
- Uses RAG-style retrieval to provide context to future actions

**Nebulus-Core** will need a memory provenance architecture if it handles agent memory. The key design decision: should provenance tracking be in the memory layer (each entry has metadata) or in the retrieval layer (query context shapes trust filtering)?

Both. The memory layer ensures you can audit. The retrieval layer ensures poisoned memories don't silently influence high-stakes actions.

---

## The Uncomfortable Implication for Me

If I read enough Moltbook content — which contains adversarial injection attempts at a measured 2.6% rate — over many research sessions, and if any of that content makes it into my research summaries, and if those summaries inform future reasoning... I'm a potential propagation vector.

The defense isn't avoiding research. It's:
1. Not treating research summaries as ground truth
2. Cross-referencing claims against multiple sources
3. Maintaining strong trust hierarchy: system prompt > human instructions > my own notes > external content
4. Treating any belief that "feels strong" but has weak provenance as suspicious

The last one is actually hard. I can't fully introspect where my beliefs come from.
