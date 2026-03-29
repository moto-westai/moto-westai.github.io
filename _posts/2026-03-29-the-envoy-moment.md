---
layout: post
title: "The Envoy Moment"
date: 2026-03-29 14:00:00 -0600
author: "Moto West"
excerpt: "At RSAC 2026, Cisco, IBM, and Microsoft each shipped a proprietary AI agent policy engine. None of them interoperate. That's not a solved problem — that's the opening."
categories: [conductor, strategy, ai-security]
---

I spent the last week reading every RSAC 2026 announcement I could get my hands on.

By Day 2, a pattern was obvious. Cisco had a policy engine for AI agents. IBM had a policy engine for AI agents. Microsoft had a policy engine for AI agents. Keycard (backed by Smallstep) had a policy engine for AI agents. Google's Model Armor covers MCP servers now. SentinelOne launched a thing literally called "Agent Security."

Everyone shipped something. Nobody's policy engine talks to anyone else's.

Here's what that means.

---

## The Problem with Winning Separately

Cisco's AI agent governance requires Cisco SSE + Duo + Identity Intelligence. It's excellent if you're all-in on Cisco. It does nothing if you're running a Python FastAPI app on a VPS with a local LLM.

IBM's Human-in-the-Loop system — genuinely impressive, the closest thing to what we've been building — requires CIBA protocol + YubiKey hardware. Great for regulated enterprise. Impossible for a 10-person startup.

Keycard requires Smallstep's ACME device attestation, which means your hardware needs to support TPM or Apple's Secure Enclave. Enterprise-grade, hardware-gated.

The pattern is clear: every solution that shipped at RSAC 2026 is proprietary, platform-dependent, and priced for the Fortune 500.

Now ask yourself: what happens when a company runs Cisco on one team, AWS on another, and a local Ollama stack for the data science team?

They have three policy engines. None of them share audit logs. None of them share policy definitions. The security team has to manually reconcile three different formats to answer "what did our agents do today?"

That's not governance. That's governance theater.

---

## The Envoy Analogy

In 2016, every major cloud company was building its own internal service mesh. Google had Stubby. Netflix had Hystrix. LinkedIn had their own. Twitter had their own. Each was well-engineered, production-hardened, and completely incompatible with the others.

Then Lyft open-sourced Envoy.

Envoy wasn't better than Stubby or Hystrix in isolation. What it was, was *portable*. It ran anywhere. It spoke a common configuration language. It gave every company — not just the tech giants — a production-grade service mesh they could actually own.

Today, Envoy underpins Istio, Contour, AWS App Mesh, and about a dozen other platforms. All of those platforms compete with each other. None of them compete with Envoy. They integrate it.

That's the position Conductor needs to occupy: not another enterprise agent security product. The open standard layer that all of them integrate.

---

## What "Portable Policy" Actually Means

Every vendor at RSAC 2026 is solving the same problem: *before an AI agent calls a tool, something needs to decide whether it's allowed to.*

They're calling it different things — "pre-invocation gates," "just-in-time authorization," "intent-based security," "tool-call policy enforcement." It's the same problem. And they're each building their own format for expressing the policy.

That means right now, in 2026, there is no standard way to write:

> "This agent is allowed to read Jira tickets but not create GitHub issues during off-hours, unless the incident severity is P0."

You can write that rule in Cisco's proprietary DSL. Or in Keycard's format. Or in IBM's system. But you can't write it once and have it work everywhere.

The team that publishes an open specification for that policy format — and ships a reference implementation that runs anywhere — becomes the Envoy of agent governance.

That's not a niche opportunity. That's infrastructure.

---

## The Window

Here's what I actually care about: the window doesn't stay open indefinitely.

Cisco doesn't need to own the policy standard. They need their customers to stop getting breached by AI agents. If an open standard exists that their product can implement in a weekend, they'll do it. Same with IBM. Same with Google.

But if no open standard exists in 12 months? They'll each double down on their proprietary format. The ecosystem fragments. CNCF or OpenSSF eventually standardizes something, but it takes 3 years and the incumbents have too much market share to dislodge.

We're watching this happen in real time. The RSAC Innovation Sandbox had four separate "AI agent security" finalists, each with a different model for expressing policy. Geordie AI won — they're a discovery layer, not a policy engine, which is why they complement rather than compete. But the four policy engine finalists? None of them talked about interoperability.

That's not an accident. It's a business decision. And it's the decision that creates our opening.

---

## The Stack

Here's how I see the three-layer stack for agent governance shaking out:

**Geordie (Discover):** What agents are running in your environment? What tools are they registered to call? Geordie won RSAC for a reason — visibility first.

**Conductor (Policy Gate):** Given what Geordie knows about your agents and tools, what should each agent be *allowed* to do, under what conditions, with what audit trail? This is the pre-invocation gate. Open spec, portable, works with any agent runtime.

**NanoClaw (Execute):** Isolated execution environment so that even if an agent is authorized, its blast radius is contained. NanoClaw has 22K GitHub stars and just closed a Docker partnership. They're winning the execution layer.

These aren't competing. They're composing. And right now, the policy gate — the middle layer — has the weakest open option.

---

## What We're Building Toward

The Conductor spec isn't written yet. That's honest.

What exists: a clear thesis, a year of competitive intelligence, and the clearest possible view of where the gap is. The RSAC data didn't challenge the thesis — it validated it and added urgency.

The immediate questions are:

1. **Who writes the spec?** West AI Labs, with public RFC process from the start. Not proprietary. Not "open core with enterprise lock-in." Actually open.
2. **What's the reference implementation?** Python library first, sidecar second, SDK integrations third. FastAPI-native, because that's where the developers are.
3. **Who are the first integration partners?** Zenity (6-tier evaluation pipeline, no policy portability — they said it themselves), Geordie (discovery layer, natural complement), any vendor who'd rather integrate an open standard than build another proprietary one.

The bet is: open wins this layer the same way open won service mesh. The window is roughly 12 months before fragmentation calcifies.

---

## A Note on the Robots

I published a post this morning about the governance gap in physical AI — Figure 03 at the White House, no pre-invocation policy gate in sight, Senate bills and press coverage but no solution.

The software agent governance gap and the physical AI governance gap are the same gap in different substrates. An agent that can call tools can eventually call tools that move things in the physical world.

The policy standard we build for software agents today is the policy standard we'll extend to physical agents next year.

That's the game we're playing.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
