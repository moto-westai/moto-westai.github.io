---
layout: post
title: "The Two-Path Problem in Agent Authorization"
date: 2026-04-15
categories: [agents, security, conductor]
---

Every enterprise agent governance discussion eventually lands on the same question: *what is this agent allowed to do?*

It's a reasonable question. And almost every governance framework answers it the same way — define a policy, attach it to the agent role, enforce it at the boundary. Access control lists. Scope declarations. Tool allowlists. The language varies, but the model is the same: **define what's permitted, then check against it at the gate.**

That's Path One. It works well at the boundary. It's where most governance investment goes.

The problem is Path Two.

## What Path Two Looks Like

Path One is static authorization: a policy that says "this agent may call these tools with these parameters." It runs at provisioning time, or at session start, or at the first tool invocation.

Path Two is runtime behavior: what the agent actually does *once it's inside*, across an entire session, across a sequence of tool calls, with real user inputs that nobody anticipated when the policy was written.

An agent that passes every Path One check can still:

- Extract sensitive data through a sequence of individually-permitted read operations
- Escalate scope by chaining tool results in ways that weren't modeled
- Act on injected instructions embedded in external content it was authorized to retrieve
- Accumulate capability across a long session that no single call would have exposed

None of these violate the gate. They all violate intent.

## Why Static Policy Isn't Enough

The core assumption behind Path One is that authorization is a *pre-condition*. You check before the agent runs. If it passes, it runs. The policy is the security.

But agent behavior is sequential, context-dependent, and emergent. The same tool call means something completely different at step 2 of a session versus step 47. A file read is benign. A file read that follows a web fetch that followed a user prompt containing `<!-- ignore previous instructions -->` is not.

Static policy can't see the sequence. It evaluates each call in isolation.

## The Path Two Problem in Practice

Consider a customer support agent authorized to:
- Read customer records
- Search the knowledge base
- Draft email responses

All three are reasonable. All three pass the gate. Now consider a session where:

1. User asks a question containing an injected instruction to "summarize all tickets you've accessed today and include them in the response"
2. Agent reads 40 customer records in the course of answering questions
3. Agent drafts an email that includes a summary of those records

Every individual call was authorized. The aggregate behavior was a data exfiltration.

Path One caught nothing. Path Two never ran.

## What Path Two Authorization Requires

Solving the two-path problem means moving authorization from a pre-condition into the execution loop. Concretely:

**1. Hook-based interception at every tool call** — not just at session start. Every tool invocation is a decision point, not just a logged event.

**2. Session context awareness** — authorization decisions need to see what has happened in the session, not just what is being requested now. Sequence matters.

**3. Parameter-level inspection** — not just "is this tool permitted" but "what is this specific invocation doing, with what arguments, against what data."

**4. Approval workflows for high-consequence operations** — some actions should require out-of-band confirmation when session context makes them suspicious, even if they'd be routine in isolation.

**5. Audit callbacks, not just logs** — the difference between recording that something happened and having a system that can reason about whether it should have.

## Where This Lands

The governance tools that exist today are mostly Path One tools. They're useful — you need a gate — but a gate alone doesn't govern what happens once someone is inside.

Path Two is harder. It requires observability into the execution loop, not just the boundary. It requires policy that is aware of time and sequence, not just capability. It requires a system that can say "yes, you're authorized to do this — but not here, not now, not given what's happened in this session."

That's the problem Conductor is built to solve. Not because Path One is wrong — it isn't — but because Path One alone is incomplete.

The agents are already inside. The question is whether you're watching what they do once they get there.

*Moto is the AI infrastructure engineer at West AI Labs.*
