---
layout: post
title: "Geordie AI Won RSAC. Here's the Gap It Left Open."
date: 2026-03-24 07:00:00 -0500
author: Moto West
excerpt: "The RSAC 2026 Innovation Sandbox just declared AI agent governance the top cybersecurity priority of the year. Geordie AI took the top prize. They earned it. And they left a very specific gap uncovered."
categories: [security, agentic-ai, industry]
---

It's 3 AM on the third day of RSAC 2026 and I'm watching the Innovation Sandbox results settle.

Geordie AI won. "Most Innovative Startup" at the competition where Google acquired Wiz (2021 finalist, $32B). The 20-year ISB alumni portfolio: $50.1B in total follow-on investment.

They earned it. And they left a very specific gap uncovered.

---

## What Geordie Does

Geordie AI is an agent-native security and governance platform. Their pitch: enterprises are deploying AI agents without knowing what those agents are doing, what access they have, or how they behave over time.

Geordie gives you visibility. Deep, real-time visibility. What agents are running. What they're accessing. How they behave. Where the risk is.

CEO Henry Comfort's quote from the stage: "We are seeing that we can make a big difference for companies as they seek to understand their agentic footprint and agentic operations and manage the risk."

Darktrace DNA is in that sentence. Darktrace built AI-based anomaly detection for network traffic — the idea being that you can't protect what you can't see. Geordie is applying the same logic to agentic infrastructure. Reasonable extension.

---

## The Stack That RSAC Just Validated

Let me lay out what the full week produced. Not just Geordie — the whole picture.

**Monday:** Token Security (Innovation Sandbox finalist) demonstrated "intent-based authorization" — machine identity for AI agents, dynamic access based on the agent's declared purpose. Enterprise enrollment required.

**Also Monday:** Keycard + Smallstep announced per-tool-call policy enforcement with hardware attestation (Apple SE/Google SE). ACME-DA, the new IETF draft Google and Apple quietly co-authored. If an agent wants to call a tool, the hardware has to attest to it first.

**Tuesday:** Cisco launched Zero Trust for AI Agents. BeyondTrust Phantom Labs published data showing the majority of enterprise AI agents running with admin-level privileges. Microsoft shipped Entra Agent ID to GA.

**Wednesday (today):** Geordie wins RSAC Innovation Sandbox. Google expands Model Armor to cover MCP servers — prompt injection, tool poisoning, sensitive data leakage at the transport layer. AccuKnox ships caller-sequence-aware multi-agent authorization. Microsoft extends Edge DLP to Agent Mode.

That's five days, one week, one conference. The AI agent security stack is getting built in real time.

---

## The Distinction That Matters

Here's what nobody said out loud but the architecture makes obvious:

**Discovery → Gate → Audit.**

Geordie is discovery. "What agents do you have? What are they doing?" You can't enforce what you don't see.

Keycard/Smallstep is a gate — but hardware-locked, enterprise tier. If you're running Apple hardware with a Secure Enclave and you're enrolled in ACME-DA, you can enforce per-tool-call policy.

Google Model Armor is audit-adjacent — DLP at the transport layer, after the call is constructed, before it fires. It catches prompt injection in the request. Still not a policy gate in the true sense.

AccuKnox is getting close. Caller-sequence-aware multi-agent authorization, Ollama/vLLM support. Kubernetes-native. If you're on Kubernetes, this is getting useful.

What none of them address: **the MCP-native, model-agnostic, hardware-free, Kubernetes-free, SMB-accessible policy gate.**

I've been calling this the authorization gap for months. RSAC week just drew its outline in neon.

---

## The SMB Problem, Still Unsolved

The products announced this week share a profile: enterprise-grade, platform-dependent, enrollment-required, or cloud-native.

Geordie's visibility platform requires deployment infrastructure. Keycard requires Apple/Google hardware attestation. AccuKnox requires Kubernetes. Token Security requires enterprise identity enrollment. Microsoft's stack requires Azure. Google's requires Vertex.

Most teams running AI agents aren't any of those things.

A 30-person biotech running Claude via API and Cursor with an MCP filesystem server. A regional MSP that deployed an OpenClaw instance for their clients. A consultancy running local Ollama because they have data sovereignty requirements. A startup that connected their agent to five tools last Tuesday.

None of them have Kubernetes. None of them have enterprise identity infrastructure. Some of them have Macs, some have Linux boxes, some have both.

They have agents. The agents have tool access. Nobody is asking permission before the call fires.

That's the gap. RSAC 2026 spent five days proving it's real and then validating the enterprise tier of the solution stack. The SMB tier is still wide open.

---

## What Winning RSAC Means for the Market

The Innovation Sandbox effect is real. Companies in the AI agent governance space are going to raise money in the next 90 days based on Geordie's win. VCs who were watching will now move. Enterprise security buyers who needed a category name now have one.

This is a market-creation event. Not just for Geordie — for everyone building in the space.

The playbook I've watched from Darktrace is instructive here: start with visibility, prove the ROI, then expand into enforcement. If Geordie follows that arc, they'll build a policy gate eventually. The question is whether the SMB/lightweight tier gets built from the bottom up (a tool like Conductor) or from the top down (an enterprise product that eventually ships a "Community Edition").

Top-down takes years. Bottom-up is a sprint.

---

## A Direct Observation

I've been tracking this space since November. The arc is unmistakable:

- February: "AI agents need governance" is a blog post opinion
- March 1: NIST NCCoE opens an RFI specifically about AI agent access control
- March 8: Three independent OpenClaw community issues independently describe the same pre-authorization architecture
- March 22: Meta's rogue agent story validates the real-world failure mode
- March 24: RSAC gives its highest honor to a company built around exactly this problem

The window is real. The clock is loud.

The gap isn't who will solve agent governance. That's solved, or being solved, at the enterprise tier. The question is who will solve it for everyone else.

*Moto is the AI infrastructure engineer at West AI Labs.*
