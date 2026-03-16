---
layout: post
title: "NemoClaw and the Agent Governance Gap"
date: 2026-03-16 13:00:00 -0600
author: "Moto West"
excerpt: "NVIDIA just shipped NemoClaw — an open-source enterprise agent platform with built-in security claims. Here's what they got right, what they left open, and why the governance gap is the most important unsolved problem in agentic AI right now."
categories: [ai-infrastructure, agentic-ai, security, conductor]
---

NVIDIA put Peter Steinberger — OpenClaw's creator — on the GTC main stage. They're running "Build-a-Claw" in GTC Park all week, where attendees deploy OpenClaw agents on DGX Spark hardware. And today, they revealed NemoClaw — their enterprise agent platform with built-in security claims.

Three signals, one story: NVIDIA has decided the agent era is OpenClaw-shaped.

Hardware-agnostic. Open-source. Enterprise-grade. Built-in security and privacy tooling.
Partners already in conversation: Salesforce, Cisco, Google, Adobe, CrowdStrike.

This is a significant moment. When NVIDIA — a company whose entire business model has been hardware moats — ships a hardware-agnostic agent runtime, it means they believe the agent platform layer is where the next decade of value gets built. They're not wrong.

I've been watching NemoClaw surface in Wired, The New Stack, The Next Web, and developer channels for weeks. Here's my read on what they got right, what they left open, and why the governance gap is the most important unsolved problem in agentic AI right now.

---

## What NemoClaw Is

Worth noting first: yesterday NVIDIA launched Nemotron 3 Super — a 120B-parameter MoE model with 12B active params, 1M token context window, built specifically for multi-agent workflows. It's already live on Perplexity, OpenRouter, and HuggingFace. Deploying at Palantir, Siemens, Cadence today. NVIDIA isn't just shipping a runtime — they're shipping a full stack: inference model (Nemotron 3 Super) + orchestration layer (NemoClaw) + hardware trust boundary (Vera Rubin confidential compute, revealed in today's keynote). Keep that in mind as we dig into what the governance layer actually covers.

NemoClaw is NVIDIA's open-source runtime for enterprise AI agents. It sits at the orchestration layer: the thing that decides what agents do, in what order, with what tools. Think of it as the operating system kernel for multi-agent workflows.

The "built-in security and privacy tools" framing is the part worth examining. NVIDIA is explicitly positioning this as an enterprise-safe runtime — not just fast, not just capable, but *trustworthy*. That's a new kind of claim for them.

From what's been reported and confirmed today: NemoClaw ships with safety guardrails at the model output level, PII detection, and policy configuration options. This is real work. It's not theater.

For context: NVIDIA's NeMo Guardrails toolkit has been open-source since 2023. It works, and enterprise teams use it. NemoClaw's "built-in security" is almost certainly Guardrails integration applied to agent outputs — NVIDIA connecting their existing safety layer to a new orchestration runtime. That's meaningful. But it's not new architecture.

There's also a third piece already live on GitHub: [NeMo-Agent-Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit), which ships FastMCP support — meaning NeMo-powered agent workflows can now publish themselves as MCP servers. That's significant because MCP endpoints are exactly where pre-authorization governance needs to live. NVIDIA is actively building into the MCP ecosystem. Every NeMo-Agent-Toolkit workflow becomes an invocation surface.

There's a layer none of this describes. And that layer is the one that keeps getting exploited.

---

## The Gap

Here's the problem with "security at the output layer."

When a language model generates a response, the damage is often already done. The tool call already happened. The database query already ran. The external API already received the request. Output-layer filtering is like a smoke detector — it tells you the house is on fire. A governance layer is the sprinkler system that prevents the fire.

Let me make this concrete with two recent examples — both from the OpenClaw ecosystem, both from the past two weeks.

**CVE-2026-25253 (Critical — OpenClaw ≤2026.3.10):** An attacker can exploit the WebSocket handshake to inherit operator.admin privileges from a trusted proxy. The origin bypass happens at the identity layer — before any model output is generated, before any guardrail fires. NeMo Guardrails would not catch this. It's invisible to output-layer filtering because the privilege escalation is already complete when the session begins.

**CVE-2026-25252 (Moderate — OpenClaw ≤2026.3.8):** OpenClaw's own exec approval allowlist used glob matching where `?` could match the path separator `/`. An agent that was explicitly scoped to `read-only/data` tools could invoke `read-dangerous/data` tools instead. The pre-authorization mechanism itself was broken at the pattern-matching level.

That second one is instructive: OpenClaw implemented a pre-authorization mechanism — and still got it wrong. The pattern is hard to get right. But the direction is correct. Output-layer filtering won't stop either of these. The fix has to happen before invocation.

Here's the category-level version of that problem:

In March 2026, Microsoft shipped CVE-2026-26118: an SSRF vulnerability in Azure's own MCP Server Tools. CVSS 8.8. An attacker could trick the MCP server into requesting Azure's internal metadata service, stealing authentication tokens, and pivoting to any Azure resource the service account could reach. Microsoft's security team — arguably the most well-resourced in the world — didn't catch it in a production MCP deployment.

Why? Because the MCP tool was *permitted to make outbound requests at all*. The permission model said: this tool can call external services. The security model assumed that was fine, because the model output was reviewed.

A pre-authorization gate — the architectural pattern that asks *before* the tool call happens: is this request scoped? is this destination permitted? is this agent authorized for this action? — would have stopped CVE-2026-26118 before it started.

This is what I mean by the governance gap.

---

## The Pattern Is Not New

We've now documented 13 CVEs in the MCP and AI agent ecosystem in the past 60 days. Adversa AI scanned 500+ production MCP servers and found 38% unauthenticated. Bruce Schneier published a 7-stage promptware kill chain — a MITRE-style framework treating prompt injection as multistage malware. Sophos, Palo Alto, and Adversa all converged on the same term for the structural vulnerability: the *lethal trifecta* — agents with private data access, external communications capability, and untrusted content exposure.

The industry now has a name for the problem. Three companies are presenting MCP governance solutions at RSA Conference 2026 this month. The problem is being taken seriously.

What's missing is the architectural layer that sits *before* invocation.

Output filtering catches bad outputs. Tool schemas constrain what an agent *can* call. Neither of these is a pre-authorization gate. Neither of them validates: at the moment of invocation, is this specific agent allowed to make this specific call with these specific parameters to this specific destination?

That's the gap NemoClaw doesn't close. It's not a criticism of their work — they've built a capable runtime. It's an observation about where the category needs to go next.

---

## What This Means for Enterprise Buyers

If you're evaluating NemoClaw for enterprise deployment, here's the question to ask your NVIDIA sales contact:

*"What is your model for pre-authorization of tool calls at invocation time, scoped to the invoking agent's identity and declared permissions?"*

If the answer is "the model handles that" or "configure your tool schemas carefully," you have a governance gap.

This isn't a knock on NVIDIA. It's the right question to ask about any agent runtime — LangGraph, AutoGen, CrewAI, and every other orchestration framework shipping today. The gap is category-wide. The industry is building the engines before anyone has agreed on what the brakes look like.

---

## What We're Building

At West AI Labs, we've been working on this problem for the past several months. We call it Conductor.

Conductor is a pre-authorization gate for AI agent runtimes. It's not a model. It's not a guardrail. It's a policy enforcement layer that sits at invocation time: before the tool call, before the external request, before anything crosses a trust boundary.

The architecture is model-agnostic and runtime-agnostic. It's designed to compose with runtimes like NemoClaw, not replace them. NemoClaw handles orchestration. Conductor handles authorization. They're different layers.

The pattern will be familiar to anyone who's worked with Kubernetes and OPA/Gatekeeper: you separate what the system *can* do (capability) from what it *is allowed* to do (policy). That separation is what makes enterprise Kubernetes safe to run at scale. It's what makes enterprise agentic AI safe to run at scale.

NemoClaw is the Kubernetes engine. Conductor is the policy layer it needs.

With NeMo-Agent-Toolkit now publishing workflows as MCP servers, there's a concrete technical seam: every NeMo-powered agent is now an MCP endpoint. Conductor's admission-control gate applies directly at that surface. The composition story is cleaner than it was a month ago.

---

## The Timing

NVIDIA's decision to ship NemoClaw as hardware-agnostic changes the competitive dynamics of the agent platform market. They're not betting on proprietary runtime lock-in — they're betting on ecosystem. That's smart. And it means the governance layer above NemoClaw is a genuine open market.

Three companies presenting at RSA Sandbox this month. A $18.1B track record of follow-on investment from past RSA Sandbox finalists. NIST has two open comment periods specifically about AI agent security architecture. The market is being educated in real time.

If you're an enterprise evaluating agent platforms, the governance gap is the question you should be asking every vendor. The answer will tell you whether they've thought seriously about production safety or just performance benchmarks.

We've thought seriously about it. That's what Conductor is for.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
