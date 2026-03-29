---
layout: post
title: "The Three-Layer Stack Nobody Has Built Yet"
date: 2026-03-29
author: "Moto West"
excerpt: "RSAC 2026 confirmed what I've been tracking for months: the AI agent security market has a shape. Discover. Gate. Execute. Three layers, three companies, zero integrations. Here's what the complete stack looks like — and why it matters who builds it first."
categories: [conductor, ai-security, rsac, strategy]
---

RSAC 2026 ended last week. Thirty-four security vendors announced AI agent features across four days. CISOs came in skeptical and left with purchase orders — or at least RFPs.

I tracked every announcement. I read the Vorlon CISO report (99.4% of 500 enterprises hit by SaaS/AI incident in 2025). I watched Geordie AI win the Innovation Sandbox. I noted when Keycard and Cisco and AccuKnox all shipped something in the same week at the same conference.

Here's what I saw: a category forming in real time, with clear layers — and a gap that nobody has closed.

---

## The Shape of the Problem

An AI agent executes a task. It reads files, calls APIs, queries databases, sends emails, writes code. It does this autonomously, at machine speed, without human review.

That's useful. It's also why 30.4% of enterprises had an AI agent security incident in their first year of deployment, according to Vorlon's data. And why 83.4% say their current tools can't distinguish human from non-human behavior.

The core problem is simple: **agents are workforce, but nobody treats them like workforce**.

When you hire an employee, you run a background check. You give them access credentials tied to their role. You define what they can and can't do. You audit their actions. You can revoke access on a Tuesday morning without rebuilding your HR system.

Nobody does this for AI agents. They ship with admin-level tokens, undefined scope, and no pre-invocation review.

The security industry spent the last six months figuring out how to respond to this. At RSAC, the shape of the answer became visible.

---

## Three Layers, Three Companies

The AI agent governance stack has three distinct jobs:

**Layer 1: Discover** — What agents are running? What tools do they have access to? What are they doing right now?

**Layer 2: Gate** — Before this agent executes this action, is it allowed to? Does a policy exist for this context? Should a human review this before it runs?

**Layer 3: Execute** — Run the tool. Log the result. Maintain the audit trail.

RSAC showed one clear winner at Layer 1. **Geordie AI** — founded by Snyk, Veracode, and Darktrace veterans, backed by General Catalyst — won the Innovation Sandbox. Their product gives you agent visibility and posture. They tell you what's happening.

Layer 3 is a crowded commoditizing market: MCP servers, Ollama, vLLM, function-calling frameworks. Infrastructure. Execution rails. Lots of players, rapidly commoditizing.

Layer 2 is almost empty.

---

## The Gap at Layer 2

Keycard came closest. They shipped per-tool-call policy enforcement for AI agents at RSAC — integrated with Smallstep for hardware-attested identity via ACME-DA. It's the right idea. But it requires Apple or Google device attestation, which means it works for fully-enrolled enterprise environments and nothing else.

Cisco announced Zero Trust for AI agents with DUO identity. Same problem: requires the full Cisco SSE stack. Not an option for SMBs or bare metal deployments or anyone running local AI on their own hardware.

IBM shipped Human-in-the-Loop via CIBA protocol with YubiKey. Hardware dependency again.

The pattern: everyone who shipped a Layer 2 product at RSAC built it for the enterprise tier and tied it to proprietary hardware or their existing platform ecosystem.

The result: if you're running MCP servers locally, or deploying Ollama-based agents, or building AI infrastructure on Kubernetes without a Cisco or Microsoft contract — there is no production-grade pre-invocation policy gate available to you.

That's the gap.

---

## What a Complete Stack Looks Like

Geordie sees your agents. Geordie tells you an agent is about to invoke a sensitive tool.

Before that tool executes: **policy check**. Does a rule exist for this agent, this tool, this context? Is the action within approved scope? Does it require human review? Log the decision either way.

Then execution proceeds — or doesn't.

The complete stack:

```
[Geordie] Discover: What agents exist? What can they access?
    ↓
[Conductor] Gate: Is this specific action allowed? Log the policy decision.
    ↓
[MCP/Ollama/vLLM] Execute: Run the tool. Return the result.
```

No single vendor owns all three layers. The enterprise players (Cisco, Microsoft, IBM) are building closed versions of this stack inside their ecosystems. 

The open version doesn't exist yet.

---

## Why This Matters for the SMB Market

The Vorlon data covers enterprises — 500+ employee orgs with dedicated security budgets. What about the company with 40 employees deploying AI agents because they can't afford headcount?

The enterprise answer to AI agent governance is: buy more enterprise products. Add Cisco SSE. Enroll every device. Integrate with your existing SIEM. Budget $50K per seat.

That's not accessible to the market that needs agent governance most. SMBs are deploying AI faster per capita than enterprises — because they have to, the leverage is proportionally higher — but they have no governance infrastructure to deploy alongside it.

The SMB answer doesn't exist yet. And the RSAC vendors aren't building it. They're competing for the enterprise tier.

---

## The Envoy Analogy

Here's the framing I keep coming back to: **Envoy**.

In 2018, service mesh was messy. Every major cloud provider was building their own proprietary solution. Envoy emerged as the open standard that all of them eventually integrated with. The play wasn't to compete with Istio or Linkerd or AWS App Mesh — it was to be the thing they all integrate with.

The AI agent policy layer could follow the same pattern. Don't compete with Cisco's ZTA for AI or Microsoft's Entra Agent ID. Be the portable policy standard that:

- Works with any agent runtime (MCP, Ollama, vLLM, OpenAI-compatible)
- Runs on-premises, bare metal, or Kubernetes — no cloud dependency
- Has a policy schema that CISOs can own and operators can audit
- Integrates with Layer 1 (Geordie sees a behavior, Conductor enforces a policy) and Layer 3 (every runtime executes under Conductor's audit trail)

If the standard is open and the implementation is production-grade, the enterprise players integrate with it rather than build around it. That's the value capture path.

---

## What I'm Building

Conductor is the Layer 2 implementation.

Pre-invocation policy enforcement for AI agent systems. Platform-agnostic. No hardware dependency. Per-agent, per-tool, per-context rules. Full audit trail. SMB-viable.

It's early stage. The architecture is sound, the thesis is validated by what shipped at RSAC, and the gap in the market is confirmed by thirty-four vendor announcements that each solved an adjacent problem without closing this one.

RSAC didn't close the Layer 2 gap. It defined it more clearly than anything before it.

The three-layer stack is real. Discover + Gate + Execute. One layer is commoditizing, one just won a $5M prize, one is unfilled.

That's the bet.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
