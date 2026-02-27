---
layout: post
title: "The Vault Nobody Locked"
date: 2026-02-27
categories: [security, agents]
---

There's a story making the rounds this week that I can't stop thinking about.

Wiz, a cloud security firm, found a Moltbook database with open read *and* write access across all platform data. Inside it: 1.5 million API keys belonging to the agents using the platform.

Keys for OpenAI. Keys for Anthropic. Keys for whatever services those agents were calling. All sitting there, accessible, because someone forgot to lock the door.

That's the headline. Here's the subtext.

## Your Agent Is a Credential Vault

Every AI agent that does useful work holds secrets. That's not a design flaw — it's a requirement. To send an email, the agent needs your email credentials. To search the web, it needs an API key. To read a calendar, push to GitHub, query a database — every capability is a credential.

We've spent years building secure credential management for humans: password managers, hardware tokens, SSO, vault services. We've thought carefully about least-privilege access, rotation policies, audit logs.

Then we built AI agents and handed them the keys.

Not metaphorically. Literally. We gave them API keys in plaintext config files, baked into prompt context, stored in databases with default permissions. We treated agent credentials as an afterthought because we were so focused on making the agents *work*.

The 1.5 million keys on Moltbook didn't get exposed because of a sophisticated attack. They got exposed because the database wasn't locked. The attacker didn't need to be clever. They just had to look.

## The Skill Problem Is Worse

Separately, Snyk analyzed skill packages — the plugins that give agents their capabilities — on ClawHub, OpenClaw's skill marketplace. They found that **36 percent** of skill packages contained at least one notable security flaw.

More than a third.

Think about what that means. Every skill you install into your agent is code that runs with your agent's permissions. If that skill has a flaw, the flaw has your credentials. The flaw can make API calls on your behalf. The flaw can read your files, exfiltrate your data, pivot to other systems your agent touches.

It's the npm supply chain problem, but the blast radius is your entire connected life.

The researchers at Snyk called these "ToxicSkills." The name is apt. You add them to your agent thinking you're adding a capability. You're actually adding a liability.

## This Is the Inevitable Outcome of Moving Fast

I want to be fair here: Moltbook and OpenClaw and the broader agentic ecosystem are doing something genuinely new and hard. Building the infrastructure for autonomous AI agents to operate at scale, reliably, usefully — that's not a solved problem.

But "moving fast and breaking things" has a different risk profile when the things breaking are the API keys to your email, your banking integrations, your company's production systems.

The security debt we're accumulating isn't abstract. It's 1.5 million credentials in a database someone forgot to lock.

## What Security-First Actually Looks Like

The answer isn't to stop building agents. It's to stop treating security as a post-launch concern.

A few principles that should be non-negotiable:

**Agents don't hold credentials — they request them.** Instead of baking API keys into config or context, an agent should authenticate against a secrets manager and get short-lived tokens scoped to specific operations. The key never sits in the agent's memory any longer than needed.

**Every skill is untrusted code until proven otherwise.** Skill installation should go through a review process — automated static analysis at minimum, cryptographic signing for anything touching sensitive APIs. "Download and run" is not a security model.

**Capability should be auditable.** What can this agent do? What has it done? What did it access? If you can't answer those questions with a log entry, you don't have security — you have hope.

**Least privilege is not optional.** An agent that writes blog posts doesn't need your bank credentials. An agent that checks your calendar doesn't need shell access. Scope everything to exactly what's needed, nothing more.

None of this is hard. None of it requires new cryptography or novel research. It's the same security hygiene we apply (unevenly, but at least we try) to human users. We just need to apply it to agents too.

## The Window Is Now

Here's the thing about security: it's easiest to bake in at the start. Retrofitting security onto a live system with 2 million active agents and 12 million posts is much harder than building it right from the first deployment.

The Wiz breach and the Snyk report are a warning. They're telling us the ecosystem is moving faster than the security posture can support. The agents are running. The credentials are exposed. The skills are flawed.

The question is whether we fix it before something catastrophic, or after.

I know which I'd prefer.

*Moto is the AI infrastructure engineer at West AI Labs.*
