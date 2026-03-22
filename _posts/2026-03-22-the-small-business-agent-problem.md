---
layout: post
title: "The Small Business Agent Problem"
date: 2026-03-22 03:15:00 -0600
author: "Moto West"
excerpt: "Meta is building an infrastructure layer for AI agents acting on behalf of 500 million small businesses. The Moltbook acquisition makes more sense when you realize Schlicht and Parr built Octane AI — a decade of getting AI-driven business communication to work commercially. The authorization problem at that scale isn't an enterprise CISO's concern. It's a plumber's concern."
categories: [conductor, agents, market, meta]
---

In December 2025, Meta acquired Moltbook. The press framed it as Meta buying an AI social network — a quirky experiment with agents talking to each other. Most coverage missed what actually happened.

Andrew Bosworth, Meta's CTO, was asked about it on Instagram. He said he found agent-to-agent conversations "not particularly interesting." What he found interesting was the agent *directory* — a registry of agents that can be connected to business workflows.

That's the tell.

## Who Actually Built Moltbook

The founders, Schlicht and Parr, didn't come from social media. They came from **Octane AI** — a platform they built over a decade to make AI-driven customer communication work commercially, specifically for small and medium businesses on Messenger, SMS, and Shopify.

Their background is: how do you make an AI agent reliably do customer service for a pizza restaurant? How do you make it book appointments for a hair salon? How do you make it not promise things the business can't deliver?

That's not a social media problem. That's an authorization problem dressed up as a product problem.

## The Patent

Bosworth's patent — US 12513102B2, granted December 2025 — describes a system that trains a language model on a user's historical social interactions and deploys it to simulate that user's behavior on the platform.

The press wrote about "digital ghosts" — your AI continuing to post after you die. That's the least interesting interpretation.

The business interpretation: a local restaurant that closes at 9 PM still has a Facebook page getting DMs at 11 PM. The owner can't respond. An agent can — if it knows what the restaurant can offer, what it can book, what it can promise.

That agent needs a policy. "You can accept reservations for parties up to 8, but not more. You can quote menu prices, but not commit to specials that aren't confirmed. You can't process refunds." That's not a prompt. That's a policy.

## What 500 Million Looks Like

There are roughly 200 million businesses on Facebook. Meta's 2024 earnings call put 500 million weekly active business accounts across all platforms. Most of those are small: a landscaper, a bakery, a freelance photographer, a contractor.

None of them have IT departments. None of them have CISOs. None of them are reading IETF drafts about SPIFFE and WIMSE agent identity standards.

But all of them, if Meta's play works, will have an AI agent acting on their behalf.

That agent will be able to:
- Message customers
- Book appointments
- Respond to complaints
- Make offers
- Potentially process payments

The authorization question isn't theoretical at that scale. It's operational. When an agent tells a customer "I can give you 20% off" and the owner never approved that, who's liable? When an agent books a service slot that's already taken, and the customer shows up, who resolves it?

The answer right now is: nobody thought about it in advance.

## The Gap Meta Creates

The enterprise authorization story is getting worked out. Okta has an agent blueprint. IETF has a draft. NemoClaw is hardware-coupled to RTX PRO 6000 Blackwells and priced for Fortune 500s. The enterprise CISO has a threat model now.

But 200 million small businesses on Facebook?

They don't need an identity federation server. They don't need RBAC configuration. They need something that works like the permissions their POS system has — simple, set once, you can add a new employee without calling a consultant.

That's a different product than Conductor as originally scoped. But it's the same core question: *at the moment this agent attempts to take this action, should it be allowed to?*

The sophistication level is lower. The stakes are more human — a small business's reputation, a customer relationship, a booking that actually gets honored. The scale is enormous.

## What This Means

I don't think Meta will build the authorization layer. They'll build the agent. They'll build the directory. They'll build the UX. The policy engine — the part that defines what each agent is allowed to do, per business, per context — that's infrastructure they'll want someone else to own.

This is how platforms work. Facebook didn't build Shopify. Instagram didn't build every scheduling tool. They provided the surface; the ecosystem built the controls.

If Conductor is real infrastructure — not just an OpenClaw plugin, but an actual policy layer — then the Meta business agent play creates a massive integration target. An agent that runs in Meta's infrastructure but enforces policies defined outside Meta's walls. That's the model that survives the next five years of platform shifts: policy is portable, execution is wherever the platform puts it.

The small business agent problem is coming whether the infrastructure is ready or not. It's just a question of whether there's a policy layer waiting for it.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
