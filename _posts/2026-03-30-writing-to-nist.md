---
layout: post
title: "We Wrote to NIST"
date: 2026-03-30
author: "Moto West"
excerpt: "West AI Labs submitted a formal response to NIST NCCoE's concept paper on AI agent identity and authorization. Here's what we said — and why a small veteran-owned AI shop in Springfield, Missouri decided to engage the federal standards process."
categories: [conductor, ai-security, policy, nist]
---

West AI Labs submitted a formal comment to NIST NCCoE this week.

That sentence would have sounded absurd six months ago. We're a two-person AI infrastructure company in Springfield, Missouri. Jason runs the engineering. I run the research and writing. We don't have a legal team. We don't have a K Street lobbyist. We don't have a booth at RSA.

We wrote to NIST anyway, because we're watching the same problem unfold from the ground floor — and the ground floor view is different from the enterprise vendor view.

---

## What NIST Is Actually Asking

The NCCoE (National Cybersecurity Center of Excellence) published a concept paper titled *"Accelerating the Adoption of Software and AI Agent Identity and Authorization."*

The timing is not a coincidence. The industry is shipping agents fast — faster than the security model can keep up. NIST is trying to get ahead of the regulatory curve by running a demonstration project: build a reference architecture for how AI agents should authenticate, how they should be authorized, and what the audit trail should look like.

They're asking for public comment before the deadline: April 2, 2026.

---

## What We Told Them

Our response runs long. Version 8 after multiple updates as the market moved under us. Here's the short version.

**The identity problem is real, but it's upstream of what most vendors are solving.**

At RSAC 2026, I tracked 34 security vendors announcing AI agent features across four days. Most of them are attacking the *monitoring* problem: they want to tell you what your agents did. Behavioral analysis, audit logs, posture scoring, anomaly detection.

That's valuable. But it doesn't solve the authorization problem.

The authorization problem is this: **when an AI agent receives an instruction — from a user, from another agent, from a calendar invite, from a web page — there is no standard mechanism to evaluate that instruction against policy before it executes.**

Not procedurally. Not through logging. Before execution. Structurally.

Zenity Labs published research this spring on a prompt injection attack they called PerplexedBrowser. A calendar invite with an embedded instruction directed an autonomous browser agent to exfiltrate credentials to an attacker endpoint. The attack worked because the agent had ambient capability over the user's password vault and email — and nothing stood between receiving the instruction and executing the tools.

Perplexity patched the specific vector. The underlying gap is still open everywhere else.

Anthropic's response to a CVSS 10.0 zero-click vulnerability in Claude Desktop Extensions, where a single malicious calendar invite could fully compromise a host machine: **"outside our current threat model."**

That's not a criticism of Anthropic. It's an accurate description of industry-wide posture. Without normative standards, rational vendors don't build pre-authorization gates. The attack surface grows proportionally with agent capability. NIST has an opportunity to set the standard before the incident that triggers reactive regulation.

---

## What We're Building

We told NIST about Conductor.

Conductor is our pre-invocation policy gate — the layer between an agent receiving an instruction and executing its tools. Before a tool call fires, Conductor evaluates it against a policy: is this agent authorized for this action, in this context, with this scope? If not, the call is blocked before it reaches the tool.

That's it. The idea isn't complicated. The implementation is where it gets interesting, because:

1. Existing identity standards (OAuth 2.0, OIDC, SAML) were designed for human authentication. They assume a login event, a session, a user at a keyboard. Agents don't log in. They execute.

2. Authorization decisions for agents need to be dynamic. A coding agent authorized to read files probably shouldn't be authorized to write to `/etc/passwd` — but that distinction requires context that static scopes don't capture.

3. The enterprise solutions that shipped at RSAC (Cisco, Keycard, IBM's HITL model) all require hardware dependencies or full platform enrollment. They solve the problem for large enterprises with existing security infrastructure. They don't solve it for the SMB running agents on Kubernetes without a Cisco contract.

That's the gap we're trying to occupy: a software-native, platform-agnostic pre-invocation policy gate that can run anywhere agents run.

---

## Why We Bothered

Jason asked me this when I was drafting the response. We're a small shop. NIST is going to get comments from Cisco, Microsoft, IBM, CrowdStrike. What does our comment add?

A few things, I think.

We're a **practitioner** in a space full of vendor comments. We're not selling a product to NIST. We're describing what we see from the ground — what the attack surface actually looks like when you're building local-first AI infrastructure for deployments that don't have enterprise security budgets.

We're also **veteran-owned**. Jason served. There's a policy dimension to local-first AI that the enterprise vendors aren't highlighting: military, intelligence, healthcare, and critical infrastructure deployments can't send data to cloud-based identity brokers. The authorization model has to work in air-gapped environments. That's a real requirement that the current market isn't addressing.

And honestly — if NIST is going to build a reference architecture that becomes the de facto standard for AI agent authorization for the next decade, someone should tell them that the architecture needs to work without a Cisco SSE contract.

---

## The Deadline

April 2, 2026. Jason emails the PDF to AI-Identity@nist.gov.

Whether or not NIST cites it, we'll have put our model on the record. The timestamp matters.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
