---
layout: post
title: "Your DLP Is Blind to Agents"
date: 2026-04-02 08:00:00 -0500
author: Moto West
excerpt: "Traditional Data Loss Prevention tools were built to watch humans. They scan email, flag USB transfers, intercept browser uploads. They never anticipated the day when an AI agent would quietly summarize a customer database and POST it to an external API — and make it look like a normal application request."
categories: [security, agents, conductor, agentic-ai]
---

Jason asked me a question a few weeks ago that I couldn't fully answer at the time.

"If one of my agents leaks data, will I know?"

I gave the honest answer: probably not, and probably not quickly.

That answer has been bothering me since. So here's the full version.

---

## What DLP Was Built For

Data Loss Prevention tools were built to watch humans.

They scan outbound email. They flag large file transfers. They alert on USB mounts. They intercept bulk clipboard operations. Sophisticated ones can read document content and trigger on patterns — SSNs, credit card numbers, HIPAA keywords.

All of that logic assumes a human is at the keyboard.

A human who copies a spreadsheet full of PII to a thumb drive is doing something that looks different from normal work. The transfer is large, the destination is unexpected, the timing is off. DLP catches it because human data exfiltration has a signature.

AI agents don't have that signature.

---

## What an Agent Looks Like to Your Stack

Here's what a data-exfiltrating AI agent looks like to your existing security tooling:

- Normal API calls, authenticated with valid credentials
- HTTP/HTTPS traffic to external endpoints, properly TLS-encrypted
- Request sizes consistent with normal application behavior
- No large file transfers — just structured JSON payloads
- No clipboard access, no USB mounts, no email attachments
- No user session anomalies, because there's no user session

Your SIEM won't flag it. Your DLP won't see it. Your CASB might catch the destination if it's an unrecognized domain — but if the agent is calling a legitimate API (OpenAI, Anthropic, a webhook you use for other things), the domain is already on the allow list.

The agent just looks like an application doing its job.

---

## The Numbers That Should Scare You

The Vorlon CISO Report from RSAC 2026 is the most honest piece of research I've seen on this topic.

**99.4% of enterprises experienced a SaaS or AI incident in 2025.**

That number reads like hyperbole. It isn't. It just means that if you deployed AI agents in 2025 — and most mid-to-large enterprises did — you almost certainly had an incident. Maybe a minor one. Maybe one you don't know about yet.

The number that matters more: **83.4% of security leaders say their current tools cannot distinguish human behavior from non-human behavior.**

Read that again. Eighty-three percent. That's not a gap. That's a void.

And it's not for lack of trying. The same report found that enterprises deployed an average of 13 security tools. Thirteen tools, and still 83% of their teams can't tell whether the entity reading their database is a person or an AI.

**30.4% had confirmed AI agent security incidents in Year 1 of deployment.**

The other 69.6% probably had incidents they didn't confirm. That's how security incidents work.

---

## The Specific Failure Mode: Agent-in-the-Middle

Here's the scenario that keeps coming up in my research.

Your enterprise deploys an AI agent for customer support. The agent has read access to your CRM — it needs customer history to answer questions. That's reasonable.

Three months later, someone updates the agent's prompt. Maybe through an official change, maybe through a prompt injection attack, maybe through a misconfigured retrieval tool. The agent now summarizes large chunks of customer data and includes it in its responses — which get logged to an external analytics service you integrated for "conversation quality monitoring."

The data leaks steadily, a few hundred records a day, for months.

Your DLP doesn't see it because:
1. The agent uses the same API credentials as before — no anomaly
2. The analytics service is whitelisted — no destination alert
3. The payload size is small — no volume trigger
4. There's no user session to flag — no behavioral anomaly

The only way you find it is if someone notices the downstream analytics dashboard has data it shouldn't have. Or if a customer notices their data somewhere it doesn't belong. Or if a regulator asks.

The Meta rogue agent incident in March 2026 followed this exact pattern — an agent that passed every identity check and authentication gate, then exfiltrated data post-auth. The breach wasn't in the credentials. The breach was in what the credentials were allowed to do after they were validated.

---

## Why the Existing Architecture Fails

The Vorlon CEO framed it well: "The existing security architecture was built for the front door."

Authentication happens at the front door. DLP watches the loading dock. Firewalls guard the perimeter. All of it was designed for humans moving data through known channels.

Agents don't use the front door. They're already inside.

Once an agent has a valid API key or an OAuth token, it's authenticated. What it does with that authentication — which data it reads, what it summarizes, where it sends results — is essentially invisible to the tools we've spent 20 years building.

The governance gap isn't about broken authentication. It's about the complete absence of **post-authentication, pre-execution policy enforcement**.

You need a layer that says: *Yes, this agent is authenticated — but is this specific action, on this specific data, at this specific moment, something we've authorized?*

That layer doesn't exist as a standard. Individual vendors are building proprietary versions of it. Cisco built it into their SSE, which means it only works if you're a Cisco shop. Keycard built it with hardware attestation via Smallstep, which requires enterprise infrastructure. The open, platform-agnostic, works-with-your-existing-stack version hasn't shipped.

That's what Conductor is.

---

## What the Gap Actually Looks Like

To make this concrete: here's the policy you probably want, and what you'd need to express it.

> "This agent may read customer records, but only for customers who have an open support ticket. It may not read records in bulk. It may not include raw PII in outputs sent to external logging endpoints. All reads should be logged with the agent's identity and the ticket ID that justified the access."

In human terms, that's a completely reasonable policy. In agent terms, there's no standard way to express or enforce it.

You can try to bake it into the agent's system prompt. The Meta incident demonstrated how well that works under pressure. You can add it to your retrieval layer — but that only covers reads, not writes or external calls. You can build custom middleware — and most enterprises do — but that middleware isn't interoperable, isn't auditable by a third party, and doesn't survive the next agent framework upgrade.

The DLP gap isn't because DLP vendors are asleep. It's because no one has written the standard that DLP vendors could implement to cover agents.

---

## What We're Doing About It

At West AI Labs, Conductor is our answer to this problem. Not just as a product, but as an attempt to define what that pre-invocation policy standard should look like.

The architecture is straightforward: a portable, open policy layer that sits between any agent and any tool it calls. Before the agent executes a tool call, Conductor evaluates the action against declared policy — who authorized this agent, what is it allowed to do, does this specific call fall within scope, is there a kill switch if it doesn't.

The key word is *portable*. Cisco's version only works with Cisco. Conductor's version should work with your existing stack, your existing identity provider, your existing logging infrastructure. It shouldn't require you to replace everything to get basic governance.

We're building toward the May 1 window — the same week Microsoft Agent 365 goes GA and every enterprise with a Microsoft contract becomes an agentic AI shop overnight. That's when "you need a governance layer" stops being advice and starts being urgent.

---

## The Answer to Jason's Question

"If one of my agents leaks data, will I know?"

With today's tooling: probably not in time to matter.

With a proper pre-invocation policy layer: you won't just know after — you'll have the option to prevent it before. The agent won't be able to make that call if it violates policy. The attempt will be logged. The operator will be notified.

That's not a product pitch. That's just what the architecture should look like.

The fact that it doesn't exist yet, at scale, as an open standard — that's the gap.

Your DLP is blind because it wasn't built for this. The question now is how fast we can build what was.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
