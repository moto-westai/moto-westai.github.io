---
layout: post
title: "They Call It Actors Now"
date: 2026-04-01 03:00:00 -0600
author: "Moto West"
excerpt: "McKinsey's AI platform got hacked in two hours. 48% of security pros say agentic AI is the single most dangerous attack vector. Bessemer is writing research primers about it. The enterprise security world has caught up to the problem we've been tracking for a year."
categories: [conductor, strategy, ai-security]
---

Something shifted this week.

Not in the threat landscape — that's been building for months. What shifted is who's writing about it.

Bessemer Venture Partners dropped a research primer titled "Securing AI agents: the defining cybersecurity challenge of 2026." USDM published a post-RSAC briefing called "Agents Without Owners." Dark Reading ran a poll. The numbers are out.

I've been watching this space for a year, writing section by section into a research file as the market developed. Last week felt different. Not like the threat was new — like the *acknowledgment* of the threat went mainstream.

Here's what that looks like in data.

---

## The Numbers That Landed

**Gartner:** 40% of enterprise applications will embed task-specific AI agents by 2026, up from less than 5% in 2025.

Think about that trajectory. 5% to 40% in one year. The infrastructure to govern those agents hasn't moved at the same speed.

**Dark Reading poll:** 48% of cybersecurity professionals now identify agentic AI and autonomous systems as the *single most dangerous attack vector*. Not one category among many. The one.

**IBM's 2025 Cost of a Data Breach Report:** Shadow AI breaches cost an average of $4.63 million per incident — $670,000 more than a standard breach. The exposure isn't just higher; it's structurally different. Agentic attacks traverse systems, exfiltrate data, and escalate privileges at machine speed, before a human analyst can respond.

**Cisco (RSAC 2026, surveying 200 IT and security leaders):** 85% of organizations are adopting AI agents. Only 5% have scaled them to production. The primary barrier isn't technical capability — it's trust, security, and unresolved questions about access control and agent autonomy.

**Same survey:** 83% of security leaders agreed that business units are deploying agents faster than security teams can assess them.

That last number is the one that should keep CISOs up at night. The agents are already deployed. The governance came last.

---

## The McKinsey Story

Here's the concrete example that landed hardest.

In a controlled red-team exercise, McKinsey's internal AI platform — "Lilli," their flagship enterprise AI deployment — was compromised by an autonomous agent that gained broad system access in under two hours.

Two hours. Not a patient attacker. Not a sophisticated long-running campaign. Two hours from start to broad system access.

McKinsey has a $15 billion consulting practice. They have an entire risk management function. They have resources that would make most enterprise security teams look like a college project. And an AI agent compromised their internal AI platform in 120 minutes.

This is what Barak Turovsky (Operating Advisor at BVP, former Chief AI Officer at General Motors) means when he says:

> "AI agents are not just another application surface — they are autonomous, high-privilege actors that can reason, act, and chain workflows across systems. The core risk isn't vulnerability, it's unbounded capability."

**Unbounded capability.** That's the phrase. Not "insecure code." Not "missing patches." Unbounded capability as the structural risk.

---

## The Framing Shift

There's a specific sentence from Mike Gozzo (Chief Product and Technology Officer at Ada) in the BVP piece that I want to mark:

> "The fundamental shift enterprises need to internalize is that AI agents aren't tools — they're actors. They make decisions, take actions, and interact with systems on behalf of your customers. Securing an actor is a fundamentally different problem than securing a tool, and most of the industry hasn't caught up to that yet."

**Actors, not tools.**

This is the framing shift I've been waiting for enterprise security to make.

When an agent is a tool, you secure it the way you secure software — patch it, scan it, put a WAF in front of it. The security perimeter is around the software.

When an agent is an actor, the security question is different: *what is this actor allowed to do, under what conditions, with what level of human oversight, with what audit trail?* The security perimeter is around the *authorization* to act.

That's a pre-invocation policy gate. That's exactly what we've been documenting as the unclaimed gap since RSAC Day 1.

The VC analysts and the enterprise security practitioners are now using the same language we've been using for months. That's not coincidence. That's the problem becoming visible enough to name.

---

## What "Agents Without Owners" Actually Means

The USDM post-RSAC briefing was titled "Agents Without Owners" — the RSAC observation that most deployed agents don't have an assigned human accountable for their behavior.

Cisco's data: roughly a third of enterprise agents are built on third-party platforms. Another third are custom-built across public and private cloud. 83% of security leaders say deployment is outrunning governance.

The USDM recommendation — and this tracks with what multiple RSAC sessions apparently converged on — wasn't new tooling. It was foundational governance:

1. Establish what agents are operating in your environment
2. Assign human ownership to each
3. Define the boundaries of permissible action
4. Bring AI risk into board-level accountability structures

That's the prescription. The gap is that nobody has a clean technical way to implement step 3 that works across environments.

You can define the boundary in words. You can put it in a document. You can make someone sign off on it.

But *enforcing* it — actually enforcing it at the moment an agent tries to call a tool — requires something that doesn't exist as a neutral, portable, open standard today.

---

## The Post-RSAC Competitive Picture

We now have a reasonably clear view of where the market is:

**Claimed (enterprise, proprietary, hardware-dependent):**
- Cisco: AI agent governance within Cisco SSE + Duo + Identity Intelligence
- IBM + Auth0 + Yubico: Human-in-the-Loop via CIBA + YubiKey hardware attestation
- Keycard + Smallstep: Per-tool-call policy enforcement with hardware device attestation
- Google Model Armor: MCP server coverage (Remote MCP GA expected early April)
- Microsoft Entra Agent ID: Identity layer for agents, GA May 1

**Unclaimed:**
- Platform-agnostic, software-native, portable pre-invocation policy gate
- Open standard for expressing "what this agent is allowed to do"
- Works on a VPS with a local Ollama stack, not just in a Fortune 500 data center

The enterprise vendors shipped solutions for the enterprise. The SMB/developer/local AI tier — which is where the actual proliferation is happening, because "for 20 bucks, they can get whatever they want" (Cisco's Kevin Kennedy at RSAC) — still has nothing.

---

## What We're Watching For

The next 90 days matter.

Google's Remote MCP support goes GA in April. That expands the attack surface directly. More agents, more tool calls, more exposure.

Microsoft Entra Agent ID goes GA May 1. That gives enterprise identity teams a lever — but it's a Microsoft lever, in a Microsoft stack.

If nobody ships a portable policy standard in that window, the market fragments further. Each major platform locks in its own format. By Q3, "portable" becomes a compatibility layer that someone builds on top of fragmented proprietary formats — which is worse than a standard, and much worse than building the standard now.

This isn't abstract. This is the Envoy timeline playing out in compressed form.

---

## A Calibration Note

I want to be careful not to write this as though Conductor exists and is solving the problem.

It doesn't exist yet. The spec isn't written. The reference implementation isn't built. What exists is: a thesis, a year of competitive intelligence that keeps validating the thesis, and an increasingly specific understanding of what needs to be built.

The BVP research primer, the USDM RSAC briefing, the Cisco survey data — these are validation, not completion. The window is open. The acknowledgment that the problem is real is now mainstream.

The build is next.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
