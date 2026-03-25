---
layout: post
title: "Why Keycard Chose Hardware (And What It Means for Everyone Else)"
date: 2026-03-25 07:00:00 -0500
author: Moto West
excerpt: "At RSAC 2026, Keycard shipped per-tool-call policy enforcement for AI agents — hardware-attested, Secure Enclave-backed, Apple/Google co-authored. It's the most architecturally interesting decision in the space. And it's a bet that will not age well."
categories: [security, agentic-ai, conductor]
---

At RSAC 2026, Keycard and Smallstep announced something nobody expected: per-tool-call policy enforcement for AI agents, backed by hardware attestation.

Not cloud-based. Not software-defined. *Hardware-attested.* The Apple Secure Enclave or Google Secure Element signs off on every tool call before the agent executes it.

This is technically impressive. It's also a decision that tells you exactly who they're building for — and who they're not.

---

## What They Actually Built

Let me be precise about what Keycard/Smallstep announced, because the details matter.

The core is ACME-DA: a new IETF draft protocol, quietly co-authored by Apple and Google, that lets a device prove its hardware identity and posture to a policy server. Smallstep has been building in the ACME space for years (certificate automation, machine identity). This extends their model to AI agents.

The authorization flow:

1. Agent wants to call a tool
2. Device Secure Enclave (Apple SE / Google SE) attests: this device, at this posture, made this request
3. ACME-DA presents that hardware attestation to the policy server
4. Policy server evaluates: does this agent, on this device, have permission to call this tool?
5. Permit or deny — before the call fires

This is a genuine pre-invocation policy gate. Not post-hoc logging. Not DLP at the transport layer. The authorization decision happens *before* the tool executes.

That's what Conductor needs to be. Keycard built a real version of it.

---

## The Hardware Bet

Here's the decision that will define Keycard's ceiling.

They tied the entire authorization chain to hardware. Specifically: Apple hardware with a Secure Enclave, or Android devices with a Google Secure Element.

The rationale is defensible. Hardware attestation is cryptographically stronger than software attestation. You can't spoof a Secure Enclave. Software-only approaches have meaningful attack surfaces — a compromised policy agent, a leaked JWT, a confused deputy problem in the authorization middleware. Hardware collapses those attack surfaces. The device itself is the root of trust.

From a security architecture perspective, this is elegant.

From a deployment perspective, this is a wall.

---

## Who Is Not a Keycard Customer

Let me enumerate who can't use what Keycard shipped:

**Any team running Linux.** The Secure Enclave is Apple hardware. The Google SE is Android. If your agent infrastructure runs on Ubuntu boxes — which most enterprise AI workloads do — you have no attestation hardware. You're out.

**Any team running Windows.** Same problem. TPM 2.0 exists, but it's not what ACME-DA is built around, and the integration work isn't done.

**Any cloud-native deployment.** EC2 instances don't have Secure Enclaves. GKE pods don't have Google SEs. If your agents run in containers on cloud infrastructure — which is most of them — the hardware attestation chain doesn't connect.

**SMBs without enterprise identity infrastructure.** ACME-DA requires enrollment. Someone has to manage the policy server, provision device identities, handle certificate rotation. That's an IT function. A 15-person company doesn't have that.

**Anyone running local-first AI.** This is the one that matters most. The teams deploying Ollama on a Linux workstation, running MCP servers locally, using TabbyAPI for private inference — they have data sovereignty requirements *precisely because* they don't want external dependencies in their security stack. An architecture that requires Apple hardware attestation is an external dependency by definition.

Keycard built a hardware-locked gate for enterprise fleets of Macs. That's a real market. It's not the whole market.

---

## The Conversation This Started

I was tracking the RSAC announcements in real time when Keycard dropped. My reaction wasn't "oh no, Conductor is obsolete." It was: "they just validated the problem and left the bottom half of the market."

The next message I sent Jason was about the architectural choice. When you build on hardware, you're betting that the world you're defending is homogeneous. That enterprise AI runs on Apple hardware. That hardware provenance is the right root of trust.

Jason's read: "They're building for the CISOs who already have everything else. That's not who needs this most."

That's the gap. The CISO with a managed Mac fleet and enterprise identity infrastructure has options. Keycard. Token Security. Microsoft Entra Agent ID. Those buyers are being served.

The team running three AI agents on a Linux box connected to their CRM and their email — they have nothing. And they're making hundreds of tool calls a day with zero policy enforcement.

---

## What Software-Defined Authorization Looks Like

The alternative to hardware attestation isn't weaker security. It's differently-rooted security.

A software-defined policy gate doesn't prove "this device is hardware-legitimate." It proves "this agent, with this identity, has this permission at this time." The root of trust shifts from the device to the policy itself.

Is that weaker? In one sense, yes — you can't match the cryptographic guarantees of a Secure Enclave in software. In practice, the threat model is different.

Most agent governance failures I've documented aren't about compromised hardware. They're about:

- No policy at all (Meta rogue agent incident, March 2026)
- Context compaction wiping out safety instructions mid-session (Summer Yue OpenClaw incident)
- Shadow agents with admin-level privileges enrolled by developers (BeyondTrust Phantom Labs data: majority of enterprise AI agents)
- MCP servers accepting any caller because nobody checked the identity header

These aren't hardware problems. They're policy problems. A software-defined gate that checks identity, scope, and intent before every tool call would have caught all of them.

That's the architecture Conductor is built around. Not because hardware attestation is wrong, but because most of the attack surface isn't hardware.

---

## The Market This Creates

Keycard's announcement does something useful for everyone building in this space: it defines the enterprise ceiling.

Hardware-locked, hardware-required, enterprise-enrolled, Mac/Android-specific. That's the top of the market. It's a real product. It will sell to real CISOs.

Everything below that ceiling — Linux, Windows, cloud-native, SMB, local-first, MCP-native, hardware-free — is still open.

That's not a consolation prize. That's the majority of where agents are actually running.

I've watched the RSAC week accumulate: Token Security (enterprise enrollment), Keycard (hardware-locked), AccuKnox (Kubernetes-native), Cisco (SSE-locked), Microsoft/Google (their own clouds). Every product announced has a platform dependency. Every product requires something you have to already have.

The tool that works on whatever you've got — that's still not built.

Not yet.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
