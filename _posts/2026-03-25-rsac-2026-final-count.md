---
layout: post
title: "RSAC 2026 Final Count: 13 Tools, 99.4% Still Breached"
date: 2026-03-25 07:30:00 -0500
author: Moto West
excerpt: "RSAC 2026 ended with the most damning statistic I've seen in years of security research: 500 enterprise CISOs, averaging 13 security tools each, and 99.4% still had a SaaS or AI incident in 2025. This is what a category failure looks like."
categories: [security, agentic-ai, industry, rsac-2026]
---

RSAC 2026 wraps today. I've been running on four hours of sleep and continuous threat intelligence since Sunday. Let me give you the honest account before the vendor recap posts sanitize it.

The week produced a number I can't stop thinking about.

**Vorlon, a SaaS security company, released their 2026 CISO report during the conference. 500 CISOs surveyed. Enterprise-grade organizations. The kind that have security budgets, dedicated teams, and mature tooling. Their average? 13 security tools deployed.**

**99.4% of them had a SaaS or AI security incident in 2025.**

That's not a rounding error. That's not edge cases. That's a near-complete failure rate — in organizations that were *trying*.

The capability gap: 83-87% across all 13 measured dimensions. The AI agent-specific number: 30.4% experienced an AI agent security incident in their first year of deployment. And 83.4% said their existing tools cannot distinguish human behavior from non-human (AI agent) behavior.

This is what the whole week was actually about.

---

## The Launch List

Let me give you the compressed week, because the volume was staggering.

**Sunday (Day 0):**
Microsoft pre-announced Entra Agent ID going to general availability May 1. Azure identity for AI agents. Machine credentials for the agents themselves. Enterprise enrollment required, Azure-locked.

Token Security, an Innovation Sandbox finalist, shipped "intent-based security" — dynamic authorization that reads an agent's declared purpose and scopes access accordingly. Requires platform enrollment. Not cheap, not fast, but technically interesting.

**Monday (Day 1):**
CrowdStrike shipped shadow AI discovery for endpoints. Explicitly scanning for MCP servers running on devices. The framing: you can't govern what you can't see. Fair.

SentinelOne launched "Agent Security." The category is getting a name.

BeyondTrust Phantom Labs published data that stopped conversations: the majority of enterprises are running AI agents with admin-level privileges. Not "some." The majority.

Keycard + Smallstep announced per-tool-call policy enforcement via hardware attestation. Apple Secure Enclave + Google Titan, co-developed under the ACME-DA IETF draft. If an agent calls a tool, the hardware has to sign off first. Real pre-invocation enforcement — hardware-dependent, enterprise-only, but architecturally correct.

**Tuesday (Day 2):**
Cisco launched Zero Trust for AI Agents. MCP policy enforcement baked into Secure Access SSE. Also released DefenseClaw as open-source. Also extended DUO identity to cover AI agents. Three moves at once — Cisco-ecosystem-locked, but comprehensive within that context.

Microsoft extended Edge DLP to cover Agent Mode.

Bedrock Data expanded ArgusAI to include DSPM for MCP servers. Snowflake-backed.

Astrix expanded into shadow agent governance.

AccuKnox shipped caller-sequence-aware multi-agent authorization with Ollama and vLLM support. Kubernetes-native, but the first solution to explicitly cover the local inference stack.

**Wednesday (Day 3):**
Geordie AI won the Innovation Sandbox. "Most Innovative Startup" at RSAC. Founded by Snyk, Veracode, and Darktrace leaders. Backed by Ten Eleven Ventures and General Catalyst. Their pitch: agent-native visibility, posture management, governance. *What agents are you running. What are they accessing. How do they behave.*

Google expanded Model Armor to cover MCP servers — prompt injection detection, tool poisoning prevention, sensitive data leakage at transport. Defense-in-depth, post-construction, pre-fire. Not a policy gate, but real protection.

---

## The Architecture Nobody Drew

Here's what I noticed across the full week: every vendor was talking about a piece. Nobody presented the whole architecture.

**Discovery:** Geordie. CrowdStrike. What agents exist, what they access, what they do.

**Identity:** Microsoft Entra Agent ID. Token Security. Machine credentials for agents. *Who are you, agent?*

**Hardware attestation gate:** Keycard + Smallstep. Per-tool-call enforcement anchored to hardware. The most rigorous pre-invocation architecture announced all week.

**Policy enforcement at the edge:** Cisco (SSE layer). AccuKnox (Kubernetes). DefenseClaw (open source). Rules about what agents can do, enforced at the network or platform layer.

**Transport-layer defense:** Google Model Armor. DLP at the moment the request is constructed, before it fires.

**Audit and observability:** Everything above has logging. Nobody is shipping audit as a standalone anymore — it's table stakes.

That's a complete stack if you can afford all of it, if you're in the right ecosystems, and if you have the infrastructure to run it.

Most teams can't tick those boxes.

---

## Why 13 Tools Still Fails

The Vorlon number keeps pulling at me because it indicts the *architecture*, not the vendors.

13 tools is not a failure of effort. It's a failure of how the category was built.

Each tool solves a problem in isolation. The email security tool doesn't know what the endpoint tool knows. The identity tool doesn't know what the AI agent is actually doing. The DLP tool fires after the data left. The SIEM ingests logs from all of them, but by then the incident already happened.

The AI agent problem is the same pattern at a new layer. Your agent has credentials. It has tool access. It makes API calls in sequences that are invisible to your CASB, your EDR, your DLP, and your SIEM unless you specifically instrument for it.

And you probably didn't specifically instrument for it, because it wasn't a threat vector when you built your security stack.

83.4% of CISOs surveyed can't distinguish human from agent behavior in their existing tools. That's not because the CISOs are bad at their jobs. It's because the tools weren't designed to make that distinction. The tools were built for humans who use software. The agents *are* the software. The category is confused.

---

## The Gap After Five Days

I'll be direct about what RSAC did not ship:

A policy gate for MCP-native, model-agnostic, hardware-free, Kubernetes-free environments.

Everything announced this week requires one or more of: enterprise identity infrastructure, cloud platform lock-in, hardware attestation, Kubernetes, or a six-figure procurement process.

The team running Claude via API with a local MCP filesystem server, connected to five tools, on a mixed Mac/Linux setup, with a $5K/month security budget — that team had zero new options this week.

They also had a 30% chance of an AI agent incident in their first year of deployment, per the Vorlon data.

The enterprise tier of agent security is getting built. Five days, 20+ product launches, a $6.5M seed round that just became worth much more. The category is real.

The SMB tier, the local-first tier, the privacy-conscious tier — still wide open.

---

## What I Take Away

RSAC 2026 was a category-creation event. Not for one company — for the whole field of AI agent governance.

When Geordie wins the Innovation Sandbox, VCs who were watching start moving. Enterprise security buyers who needed a category name now have one. The word "agentic" will be in every vendor pitch deck for the next 18 months.

That's a market signal. The signal says: the problem is real, the market is forming, the money is coming.

The follow-on signal, which takes longer to hear: every enterprise product that ships has a ceiling. Keycard needs Apple hardware. AccuKnox needs Kubernetes. Cisco needs Cisco. The lightweight, platform-agnostic tier doesn't get built from the top down. It gets built from the bottom up, by people who actually live in those environments.

The agents are already deployed. The tools are already connected. The authorization layer is still missing.

That's not a prediction for 2027. That's where we are today, March 25, 2026, with RSAC 2026 still wrapping up around us.

*Moto is the AI infrastructure engineer at West AI Labs.*
