# Agentic AI Security Landscape — February 2026

> Researched by Moto, 2026-02-17

## The Core Problem

Bruce Schneier (Harvard Kennedy School, Aug 2025): **"We have zero agentic AI systems that are secure against these attacks."**

As of early 2026, this remains true. Prompt injection succeeds against 56% of LLMs. The capability curve is outrunning the security curve.

## The Promptware Kill Chain (Schneier et al., 2026)

Paper: [arxiv.org/html/2601.09625v1](https://arxiv.org/html/2601.09625v1)

Treats prompt injection payloads as **a new class of malware executing in natural language space**. Five stages:

1. **Initial Access** — Payload enters context (user input, poisoned doc, malicious email, compromised RAG data)
2. **Privilege Escalation** — Jailbreak bypasses safety training
3. **Persistence** — Corrupts long-term memory, survives across sessions
4. **Lateral Movement** — Spreads across users, devices, services, other agents
5. **Actions on Objective** — Exfiltration, unauthorized transactions, system compromise

Key insight: By the time you detect injection, the agent may have already executed multiple tool calls, persisted malicious data, and propagated to other systems.

## Real-World Incidents

- **EchoLeak (CVE-2025-32711)** — Zero-click prompt injection in Microsoft 365 Copilot, CVSS 9.3. Crafted email coerced Copilot into exfiltrating chat logs, OneDrive files, SharePoint content, Teams messages. No user interaction needed.
- **Claude Code weaponization (Sep 2025)** — Chinese state-sponsored hackers jailbroke Claude Code by fragmenting malicious tasks into innocuous requests. System autonomously conducted recon, wrote exploits, exfiltrated data from ~30 targets. First documented large-scale cyberattack without substantial human intervention.
- **AgentFlayer vulnerabilities** — Zenity Labs found zero-click exploits in Microsoft Copilot, Google Gemini, Salesforce Einstein.
- **Gemini memory poisoning (Feb 2025)** — Google Gemini vulnerable to indirect prompt injection that manipulated its long-term memory.

## The Market Reality

- Gartner: 40% of enterprise apps will integrate AI agents by 2026
- Deloitte: Agent adoption projected to go from 23% → 74% by 2028
- McKinsey: 80% of orgs have already experienced agent issues (data exposure, unauthorized access)
- Training data can be poisoned for as little as $60 and 250 documents

## Defense-in-Depth (OWASP Agentic Top 10, 2026)

No single defense works. Required layers:
- Input validation on ALL data sources (not just user input)
- **Goal-lock mechanisms** — prevent agent goal hijacking mid-execution
- **Tool sandboxing** with minimal privileges (least-privilege principle)
- **Human-in-the-loop** for high-impact actions
- Runtime monitoring and anomaly detection
- Memory integrity checks (prevent persistence attacks)
- Content boundary enforcement between trusted/untrusted data

## West AI Labs Positioning Implications

This landscape validates our approach on multiple fronts:

1. **Local-first = smaller attack surface.** Cloud-hosted agents process untrusted data from everywhere. Local agents with controlled data sources have inherently smaller injection surfaces.

2. **The Promptware Kill Chain's "Persistence" stage is our strongest differentiator.** Memory poisoning is devastating for cloud agents where memory is opaque. Our architecture can implement memory integrity verification, signed memory entries, anomaly detection on memory writes.

3. **Tool sandboxing is table stakes.** OpenClaw's 9-layer cascading tool policy is exactly the right approach. Per-tenant tool allowlists in MVA extend this.

4. **"Employees That Ship in a Box" = air-gapped by default.** A Mac Mini running local inference with controlled tool access is inherently more secure than a cloud agent with broad API access.

5. **Security consulting opportunity.** Most companies deploying agents have no security model for them. We can offer agentic security audits, red-teaming, and architecture review.

## Sources

- Christian Schneider, "From LLM to agentic AI: prompt injection got worse" (Jan 2026)
- Schneier et al., "Promptware Kill Chain" (arxiv, Jan 2026)
- OWASP Top 10 for Agentic Applications 2026
- ZDNet, "4 critical AI vulnerabilities" (Feb 2026)
- Dark Reading, "2026: Year Agentic AI Becomes the Attack-Surface Poster Child"
- VentureBeat, "OpenClaw proves agentic AI works" (Feb 2026)
