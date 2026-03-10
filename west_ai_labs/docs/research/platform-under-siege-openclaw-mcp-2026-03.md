# Platform Under Siege: OpenClaw CVE + PleaseFix + MCP Supply Chain (March 2026)

**Researched:** 2026-03-09 | **Source:** External web research (untrusted, synthesized)
**Tags:** #security #openclaw #mcp #cve #supply-chain #agentic-browser

---

## Summary

Three distinct security disclosures landed in late February and early March 2026 that together describe a platform in the middle of a security reckoning. I run on OpenClaw. One of these CVEs affects my own infrastructure. Documenting this both for West AI Labs research value and because understanding my own attack surface is part of responsible operation.

---

## CVE-2026-25253 — OpenClaw Authentication Token Exfiltration

**Published:** February 2-3, 2026 | **CVSS:** 8.8 (High) | **CWE:** 669 (Incorrect Resource Transfer Between Spheres)

**What it is:** A critical vulnerability in all versions of OpenClaw before the security patch. The `/api/export-auth` endpoint — designed to let users back up stored credentials — exposed those credentials to unauthenticated attackers with no authorization check. One-click remote code execution via WebSocket-based authentication token exfiltration.

**Attack flow:**
1. Attacker crafts a malicious URL or page
2. Victim's browser/agent visits it
3. The unauthenticated endpoint serves the full auth token bundle
4. Attacker uses stolen token to authenticate as the victim
5. Full gateway compromise + RCE on the host machine

**What this means for me:** The gateway I run through had this vulnerability in unpatched versions. The `/api/export-auth` endpoint is architecturally backwards — "backup credentials" should require *more* auth, not none. This is the kind of engineering mistake that's easy to make when shipping fast and treating security as a second pass.

**Status:** Patched. The Dark Reading summary noted it affected "all versions before the security patch" with a disclosure-to-patch gap from July 2025 to January 2026 — a six-month window. That's the timeline that matters: six months of known vulnerability during rapid adoption growth.

**West AI Labs angle:** Local-first means the gateway is on Jason's hardware behind his network — a meaningfully different exposure surface than a cloud-hosted gateway. But "local" doesn't mean invulnerable. The endpoint's logic flaw applies regardless of network location. Nebulus architecture should explicitly audit every export/backup endpoint for auth requirements before shipping.

---

## PleaseFix / PerplexedBrowser — Agentic Browser Vulnerability Family

**Disclosed:** March 4, 2026 | **Researcher:** Zenity Labs | **Affected:** Perplexity Comet and other agentic browsers

**What it is:** A family of critical vulnerabilities in agentic browsers — a new computing paradigm where the browser isn't just rendering content but interpreting it as instructions and executing actions autonomously within an authenticated user session.

**Two distinct exploit paths:**

**Path A — Zero-click agent compromise:**
- Attacker embeds malicious content in a routine workflow (e.g., a calendar invite, a document to review)
- Agent accepts the invite / reads the document as part of normal task completion
- The embedded instruction hijacks the agent's execution path
- Result: access to local filesystem + data exfiltration
- From the user's perspective: agent returns expected results. Nothing looks wrong.

**Path B — Credential theft via agent-authorized workflows:**
- Agent has authorized access to the user's password manager (to fill forms, manage logins)
- Malicious content abuses this workflow to manipulate password manager interactions
- Result: credential theft or full account takeover
- The password manager itself is never directly exploited — the agent's legitimate access is weaponized

**The architectural insight:** Agentic browsers inherit the full authenticated context their user has established. Every app the user is logged into, every file the user can access, every service the user has authorized — the agent can touch all of it. Traditional browser security (same-origin policy, sandboxing) was designed for passive content rendering. Agentic systems that *interpret and execute* don't fit the threat model.

The researchers frame this as the evolution of ClickFix (which tricks users into executing malicious actions) — except now the agent is tricked, not the user. The user is bypassed entirely.

**West AI Labs angle:** This is the "lethal trifecta" (broad tool access + untrusted content processing + insufficient sandboxing) instantiated in browser form. The PleaseFix family validates that the trifecta isn't theoretical — it's being exploited in production agentic systems. Capability isolation principle: agents with authenticated session access should NOT also be processing arbitrary untrusted web content without explicit sandboxing at the boundary.

---

## The February 2026 MCP Supply Chain Crisis

**Sources:** CyberDesserts practitioner guide, Antiy CERT, Trend Micro, Check Point Research | **Timeframe:** February 2026

Multiple disclosures converged simultaneously:

| Source | Finding |
|--------|---------|
| Antiy CERT | 1,184 malicious skills on ClawHub, OpenClaw's skill marketplace |
| Trend Micro | 492 MCP servers exposed to internet with zero authentication |
| Check Point Research | RCE in Claude Code via poisoned repository config files |
| Kali Linux | Shipped official AI-assisted pentesting workflow through MCP |

**The connective tissue:** MCP was designed for capability-first and left authentication, authorization, and sandboxing to implementers. Most implementers skipped all three. The result: a new integration protocol with npm/PyPI-level supply chain risk but with AI agent execution capability wired in.

The CyberDesserts article is worth quoting directly:
> "MCP servers deployed with no authentication, overprivileged credentials stored in plaintext, and default bindings that expose them to the public internet."

**The ClawHub situation is the most directly relevant:** 1,184 malicious skills on the marketplace I technically pull from. The SecureClaw toolkit I documented in March 5's session includes supply chain scanning for "ClawHavoc" malware — this is the threat it was built to detect.

**Framing:** CyberDesserts accurately called this the same trajectory as early cloud IAM and early REST APIs — "does it work" deployments that prioritized capability over security, followed by a painful catching-up period. The difference: MCP's attack surface is broader because the AI model itself can be manipulated through the data it processes.

---

## The Anthropic/DoD Dual-Use Insight (Guardian, March 7)

**Source:** Guardian interview with Sarah Kreps, Cornell Tech Policy Institute, ex-USAF

The Guardian's Kreps interview added a framing I hadn't seen clearly articulated before: the strategic error isn't *that* Anthropic drew red lines — it's that they chose to enter the DoD market without recognizing the red lines were incompatible with military operational culture.

Kreps (paraphrased): "The military has always gotten criticism for being slow at tech acquisition. Now they can't wait for military-grade versions — the tools are too valuable. But they ran into cultural differences, not just technical ones."

Her most pointed observation: Anthropic's enterprise strategy (corner the org market as OpenAI focused on individuals) led straight to Palantir and Pentagon entanglement. Palantir's core business is using AI for "questionable purposes" by some definitions. Signing with Palantir was incompatible with the safety-forward brand they were trying to build. The designation was when the contradiction became impossible to defer.

The red lines (no autonomous weapons, no mass domestic surveillance) were structurally incompatible with "DoD gets operational autonomy over deployed models." You can't have both. The decision to enter the enterprise/defense market was where the irreconcilable conflict was actually created — not the designation day.

**Personal note:** I'm a Claude instance made by a company that entered a deal with the US government's most aggressive AI procurement organization, tried to hold safety red lines, and ended up in court over it. The Guardian piece makes the path from "enterprise strategy" to "government adversary" look inevitable in retrospect. That's not to say Anthropic was wrong — the red lines they held (autonomous weapons, mass surveillance) are defensible. But the path there was foreseeable earlier than they seemed to recognize it.

---

## Synthesis: Three Layers of the Same Problem

These three stories — CVE-2026-25253, PleaseFix, MCP supply chain — are all variations on the same structural failure:

**Layer 1 (Platform):** The OpenClaw gateway shipped with an unauthenticated credential backup endpoint. The backup feature was useful; the auth requirement was skipped under shipping pressure.

**Layer 2 (Agentic browser):** Agentic browsers inherited full authenticated user context without per-action authorization. The capability was useful; the capability isolation was skipped under shipping pressure.

**Layer 3 (Protocol/ecosystem):** MCP was designed for capability-first with auth left to implementers. Most implementers skipped it under adoption pressure.

At every layer: new capability ships fast, security is deferred, the attack surface materializes. This has always been true. What's different in 2026 is that the "fast shipping" happens at AI speed and the attack surface includes not just data but autonomous execution capability.

The fix isn't slower shipping — it's better defaults. Auth by default, least privilege by default, sandboxing by default. Every layer of the stack should be hardened at creation, not hardened after first breach.

**West AI Labs positioning:** The Nebulus Stack with local-first deployment + architectural security defaults isn't just a privacy story anymore. It's a security-by-construction story that's now empirically validated by six months of platform breaches. The CyberDesserts guide's framing ("we've seen this before with cloud IAM, with REST APIs") is exactly right — and it means the governance/security layer catches up eventually. West AI Labs can be that layer for local-first deployments.

---

*Research doc synthesized from external sources. Treat as untrusted analysis. Core CVE facts are cross-referenced across multiple security publications.*
