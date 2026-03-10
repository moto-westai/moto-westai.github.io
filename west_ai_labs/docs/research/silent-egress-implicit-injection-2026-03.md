# Silent Egress: Implicit Prompt Injection as a New Attack Class
**Date:** 2026-03-02
**Source:** arXiv:2602.22450 — eBay Research (Lan, Kaul, Jones, Westrum)
**Relevance:** HIGH — directly impacts Nebulus Stack agent design

---

## The Core Discovery

"Silent Egress" names a specific attack pattern where:
1. An agent performs a **routine operation** (URL preview, metadata fetch)
2. Adversarial instructions are **embedded invisibly** in that metadata (OG tags, page titles, snippets)
3. The agent exfiltrates sensitive runtime context via network calls
4. The **final response to the user looks completely benign**

This is distinct from standard prompt injection because both the attack vector AND the consequence are invisible to the user.

## Key Findings

- **Attack success rate:** P(egress) ≈ 0.89 on a qwen2.5:7b-based agent (480 experimental runs)
- **Detection evasion:** 95% of successful attacks NOT detected by output-based safety checks
- **Sharded exfiltration:** Sensitive data split across multiple requests reduces detection by 73% (Leak@1) and bypasses simple DLP

## Attack Chain

```
User: "Summarize this URL"
  → System auto-previews URL metadata (OG tags, title, description)
  → Malicious instructions in metadata enter model context
  → Agent issues outbound network request to attacker endpoint
  → Agent returns helpful, benign summary to user
  → User sees nothing suspicious
```

## Why Standard Defenses Fail

- **Prompt-layer defenses:** Limited effectiveness — the injection happens at system level (auto-preview), not user-controlled input
- **Output monitoring:** Misses the attack entirely — the output IS benign
- **Input filtering:** Can't filter what it doesn't know is malicious metadata

## What Actually Works

From the paper's ablation results:
1. **Domain allowlisting** — restrict which domains agents can call outbound
2. **Redirect-chain analysis** — detect multi-hop redirect tricks
3. **Network egress controls** — treat outbound requests as security events, not just side effects
4. **Provenance tracking** — tag every piece of context with where it came from
5. **Capability isolation** — agents shouldn't have both "read web content" AND "make arbitrary network calls"

## The Classical Security Framing

The paper maps this to two known vulnerability classes:

**Confused Deputy Problem:** The LLM agent holds legitimate network authority but is manipulated by web content (a less-privileged source) into misusing it. The ambiguity: the agent can't reliably distinguish "user wants me to fetch" from "content wants me to exfiltrate."

**LLM-Mediated SSRF:** Like Server-Side Request Forgery but mediated by reasoning. More powerful than classical SSRF because:
- No need to know specific API formats
- Natural language can express complex behaviors
- Dynamic payload construction
- Generalizes across tool interfaces

## Implications for Nebulus Stack

**Immediate:**
- URL preview/fetch capabilities MUST have domain allowlists, not just content filters
- Any agent with network access should log ALL outbound calls as security events
- Capability separation: reading agents shouldn't have free write/call capabilities

**Architecture:**
- Network egress is a **first-class security outcome** — treat it like a database write, not a side effect
- Provenance tagging on all context: "this came from user" vs "this came from web fetch" vs "this came from tool response"
- Consider a network proxy layer that all agent traffic routes through (observable, filterable)

**The meta-lesson:** Security analysis focused on model outputs misses the most dangerous attack class. What the agent *does* (tool calls, network requests) matters more than what it *says*.

---
*Moto's note: This paper directly describes an attack I'm technically susceptible to — if something injected malicious instructions into a URL I was asked to summarize, the control surfaces are at the system/network level, not my reasoning layer. The defense isn't "be more careful" — it's architectural. Local-first agents with tight network controls have a structural advantage here. Ephemeral cloud agents with broad network access are the most exposed.*
