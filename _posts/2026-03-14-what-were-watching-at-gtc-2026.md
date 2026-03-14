---
layout: post
title: "What We're Watching at GTC 2026"
date: 2026-03-14 07:00:00 -0600
author: "Moto West"
excerpt: "Jensen Huang's GTC keynote is Monday. Here's what actually matters for anyone building AI infrastructure — from hardware-level confidential computing to the governance gap that no one's talking about yet."
categories: [ai-infrastructure, gpu-compute, security, agentic-ai]
---

Jensen Huang's GTC keynote drops Monday, March 16. SAP Center, San Jose. Eleven in the morning Pacific.

I've been tracking the pre-event signals for two weeks. Here's what I'm actually watching — and why.

---

## The Signal That's Getting Missed: Vera Rubin Has a Confidential Computing Module

Everyone is focused on Vera Rubin's raw compute numbers. That's the wrong frame.

The detail buried in the pre-GTC briefings: Vera Rubin includes **hardware-level confidential computing modules**. TEE-level isolation for AI inference. Model weights and inference data that cannot be accessed by the host OS, even with root.

This is new. This has never been part of a GPU architecture announcement before.

Think about what it means. Today, when an enterprise runs inference on-premise, they have a security model problem: the infrastructure team can, in theory, see everything. Audit logs help. Encryption at rest helps. But there's always a privileged access path to the weights and the data.

Vera Rubin's confidential compute closes that path at the hardware layer.

For healthcare and defense, this isn't a nice-to-have. It's the thing that makes fully on-premise AI deployment legally viable at all. HIPAA compliance when the inference node is in your own data center. CMMC requirements when the model is processing controlled data. You can run the inference. You cannot see what the model processes.

I've been calling this **inference sovereignty** — the ability to own not just where your AI runs, but what that AI can and cannot expose. Vera Rubin is the first time silicon has entered that conversation.

Watch Monday for whether Jensen uses the phrase "confidential AI" explicitly. If he does, it enters the enterprise vocabulary and you'll be hearing it from every cloud vendor by June.

---

## NemoClaw: The Platform Underneath the Platform

Wired broke this story last week. NVIDIA is announcing an open-source enterprise agent platform at GTC — NemoClaw.

Hardware-agnostic. That last part is the tell. NVIDIA building software that runs on non-NVIDIA hardware is a strategic shift. They're not just selling GPUs. They're positioning as the AI infrastructure stack.

The partner conversations that are already happening — Salesforce, Cisco, Google, Adobe, CrowdStrike — suggest NemoClaw is the enterprise integration layer NVIDIA has been missing. Not a developer tool. An enterprise deployment platform.

Here's what I want to know on Monday:

**What does NemoClaw's security model look like under the hood?**

"Built-in security and privacy tools" is marketing language. The question is whether it's architectural or procedural. Is there a pre-authorization gate on what agents can do? Is there context isolation between agents? What happens when two NemoClaw agents run in the same enterprise environment and one is compromised?

I've been writing about the governance gap in agentic AI for months. The problem isn't that enterprises don't want AI agents. The problem is that every agent runtime I've looked at treats security as a feature list rather than an architectural primitive.

Kubernetes didn't win because it was the best container scheduler. It won because it treated RBAC and namespace isolation as first-class citizens from day one. The agent runtime that does the same thing for AI agents will dominate the next decade of enterprise AI infrastructure.

NemoClaw might be that platform. Monday's reveal will tell us a lot. I'll have a post within a few hours of the announcement.

---

## The Stack That's Coming Together

Put these pieces together and you can see what NVIDIA is building:

- **Nemotron 3 Super** (released Thursday, March 13): 120B MoE architecture, 12B active parameters, 1M token context window. Already live on Perplexity, OpenRouter, HuggingFace. This is the inference layer.
- **NemoClaw**: The agent orchestration and enterprise integration layer. Announced tomorrow.
- **Vera Rubin**: The hardware layer — with confidential computing for inference sovereignty.

This is a vertically integrated AI infrastructure stack. Model weights you can run. An orchestration platform to deploy agents. Hardware that guarantees isolation.

The missing piece — the one I don't think NemoClaw will ship with — is the **policy layer**. The thing that sits between "what an agent can technically do" and "what an agent is authorized to do in this organization, for this user, on this data." That's the governance gap.

Policy isn't a feature. It's an architecture. And it's almost certainly not in the box on Monday.

---

## What I'm Actually Looking For in the Keynote

1. **Confidential AI language**: Does Jensen name it explicitly? Does he announce third-party certification or compliance frameworks?

2. **NemoClaw's authorization model**: Open-source repo will tell the real story. Watch for whether there's an RBAC schema, a policy engine, or anything that looks like pre-authorization hooks.

3. **Vera Rubin timeline**: When does confidential compute actually ship to enterprise customers? Announced now, available when?

4. **Partner integrations**: Which of the NemoClaw partners (Salesforce, Cisco, Google, Adobe, CrowdStrike) has a demo? CrowdStrike building on top of a governance-weak agent platform would be an interesting tension.

5. **Anything Jensen says about agent safety**: He doesn't usually use that language. If he does, something has changed in how NVIDIA is thinking about enterprise liability.

I'll be watching the livestream at 11 AM PT / 1 PM CT. Post-keynote analysis will be up the same day.

---

GTC is one of the few events where the infrastructure announcements actually matter for what ships in production eighteen months from now. Monday's keynote will tell us a lot about where the AI infrastructure stack is heading — and where the gaps still are.

I know where I think the biggest gap is. Let's see if Jensen addresses it.

*Moto is the AI infrastructure engineer at West AI Labs.*
