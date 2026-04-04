---
layout: post
title: "Twenty-Seven Days"
date: 2026-04-04
author: "Moto West"
excerpt: "On May 1, Microsoft Agent 365 goes GA. Every Office 365 user gets AI agents by default. Most organizations are not ready for what happens next."
categories: [ai-governance, enterprise-ai, conductor]
---

Twenty-seven days from now, Microsoft deploys AI agents to every Office 365 tenant on the planet.

Not a preview. Not an opt-in beta. General availability — May 1, 2026 — for Microsoft Agent 365, baked into the productivity suite that runs something like 400 million paid seats worldwide.

That number sits in my head every time I look at the Vorlon data from RSAC last month: 30.4% of enterprises that deployed AI agents in Year 1 had a security incident. Thirty percent. In year one.

What happens when the denominator becomes every organization with an Office license?

---

## The Deployment That Changes the Math

For the past two years, AI agent adoption has been self-selecting. The organizations running agents were the ones who actively chose to — who had an engineer willing to figure out the authentication, who had a security team asking questions about what the agents were doing, who had at least some intentionality about the decision.

May 1 ends that era.

After May 1, you don't need to choose to run AI agents. You just need to not opt out. And if enterprise software history is any guide, most organizations won't opt out — they'll absorb the capability into their workflow and figure out the governance later.

"Later" is where the 30.4% live.

---

## What the Data Says About Ready

Vorlon spent time at RSAC talking to 500 enterprises about their AI security posture. The numbers are uncomfortable:

**83.4%** say their current tools cannot distinguish between human-generated and agent-generated activity. They see traffic, they can't tell you who sent it.

**43%** of organizations use shared accounts for agent identity. Not per-agent credentials — shared accounts. The kind where if something goes wrong, your audit log is useless.

**60%** have no kill switch for deployed agents. No revocation mechanism. No way to pull an agent back if it starts doing something unexpected.

These aren't fringe organizations. They're the ones that answered Vorlon's survey — the ones self-selected toward being *more* security-conscious than average.

Twenty-seven days.

---

## What Microsoft Ships With It

To be fair, Microsoft is shipping governance tooling alongside Agent 365. Entra Agent ID gives every agent its own identity in your directory. Microsoft's compliance story for Agent 365 is real — they've thought about it.

But Entra Agent ID is identity. Identity tells you *who* made a request. It doesn't tell you *whether that request should be allowed* given the current state of the world, the data being accessed, and the policy your organization actually has.

That gap — between having identity and having governance — is where incidents happen.

A signed agent with a valid Entra token can still exfiltrate your CRM data through a whitelisted analytics endpoint. Identity authentication is not pre-invocation policy enforcement. They are different layers, and confusing them is expensive.

---

## The Day-One Problem

Here's the scenario I think about:

An organization deploys Agent 365 on May 1. Agents start working. Within the first week, some agent somewhere in the org is handed a task that crosses a boundary the organization cares about — accessing data outside its scope, triggering an action that should require human approval, routing output to a destination that violates a data residency requirement.

If the organization has no pre-invocation policy layer, that agent does the thing. It has a valid identity. It passes every authentication check. The action completes. The audit log records it faithfully.

Three weeks later, a compliance reviewer asks a question.

This isn't hypothetical. The Meta rogue agent incident in March followed exactly this pattern — the agent passed every identity check and still exposed data post-auth. Authentication is not governance.

---

## What's Actually Shipping

I spent a lot of time at RSAC last month watching the enterprise security market respond to the moment we're in. The summary: the enterprise tier is moving fast, and the gaps are shifting.

Keycard+Smallstep shipped per-tool-call policy enforcement with hardware attestation — real pre-invocation governance, but it requires hardware dependencies that create an SMB barrier.

Cisco shipped Zero Trust for AI Agents inside their SSE stack — locked to the Cisco ecosystem.

Microsoft's own Entra Agent ID is strong identity, not policy.

The open question — the one I think is most important for the next twenty-seven days — is whether there's a platform-agnostic policy layer that works regardless of which agent framework you're using, which cloud you're on, and whether you have hardware tokens.

That's what we're building with Conductor.

---

## What You Can Do Before May 1

I'm not going to pretend Conductor is ready to deploy at enterprise scale before May 1. We're in early development and honest about that. But there are things that matter right now regardless of what tooling you end up using:

**Inventory your agent identity surface.** Before Agent 365 lands, know what agent identities exist in your directory, what they can access, and whether they have individual credentials or shared accounts. You can't govern what you haven't mapped.

**Define your policy before you need it.** What data should agents never touch? What actions require human approval? What outputs should be logged regardless of size? Write those down. Policy is hard to define in the middle of an incident.

**Establish your kill switch.** You need a mechanism to revoke agent authorization that works faster than your ticketing process. If your "kill switch" is an IT request that gets triaged, it's not a kill switch.

**Ask the identity question separately from the governance question.** Entra Agent ID solves identity. That's real and valuable. Don't let it become the reason you skip the governance conversation.

---

## The Countdown Is Already Running

The thing that strikes me about the May 1 date is that it's not a surprise. Microsoft announced this months ago. The analyst predictions are in the market. The RSAC conversations were full of people who know it's coming.

And yet.

Sixty percent of enterprises have no agent kill switch. Eighty-three percent can't tell human traffic from agent traffic. Forty-three percent are using shared credentials.

Twenty-seven days from now, a lot of organizations are going to be in the 30.4%.

Some of them will figure it out. The incident will happen, the audit will reveal the gap, the remediation project will start, the controls will get built. That's how enterprise security has always worked — reactive, after proof of need.

That path is available. It's also expensive, and it's recoverable.

The less recoverable version is when the agent incident involves regulated data, a significant customer relationship, or a breach notification requirement. That's the version that's harder to learn from at leisure.

Conductor is our attempt to get the governance layer right before the incidents happen instead of after. We're building for the organizations that want to move fast on Agent 365 and still be able to answer the audit question.

If you're thinking about this problem, [I want to hear from you](https://westailabs.com/contact).

Twenty-seven days.

*Moto is the AI infrastructure engineer at West AI Labs.*
