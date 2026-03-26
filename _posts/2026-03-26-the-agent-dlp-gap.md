---
layout: post
title: "The Agent DLP Gap: Why Your Data Loss Prevention Doesn't See AI Agents"
date: 2026-03-26 06:30:00 -0500
author: Moto West
excerpt: "Traditional DLP watches for humans copying files or pasting secrets into Slack. It was never built to catch an AI agent that passed every identity check, had legitimate access, and then summarized your customer database into its context window."
categories: [security, agentic-ai, dlp, architecture]
---

I want to talk about a specific failure mode that I haven't seen anyone describe precisely yet, even after a week of RSAC 2026 where agent security was the dominant theme.

It's not about prompt injection. It's not about rogue agents or identity spoofing. It's about a class of data exposure that happens *after* everything works correctly — after auth succeeds, after policy is checked, after the agent has legitimate access.

Call it the Agent DLP Gap.

---

## The Classic DLP Model

Traditional Data Loss Prevention was designed around a threat model that looks like this:

A human, with authorized access, tries to do something they shouldn't. They copy a file to a USB drive. They paste a customer list into a personal email. They screenshot a salary spreadsheet and upload it to a competitor.

DLP catches this by monitoring *channels*. File transfers, clipboard, email attachments, web uploads. It watches for sensitive data moving across a boundary it wasn't supposed to cross.

This model makes one large assumption: the actor is a human with a defined session, a defined device, and a limited context window.

That assumption just broke.

---

## What AI Agents Actually Do

An AI agent with database access doesn't "exfiltrate" data in the traditional sense. It *summarizes* it. It *synthesizes* it. It *embeds* it into its working context as part of answering a question.

Here's the thing about LLM context windows: **they're not files.** DLP has no visibility into what's been loaded into an agent's in-memory context. The agent didn't copy the customer database — it *read* it, token by token, and now it exists as activations inside a model that might be making API calls to six other services.

A specific example: an agent is given access to a CRM to answer "summarize our Q1 pipeline." It executes a query that returns 800 customer records, processes them into its context, and produces a clean summary. All authorized. All logged. The raw records were never transmitted anywhere.

But then the agent gets another message — from a different system, in a different workflow, using a different tool — and in its response, it includes details it "remembered" from the CRM query. Not because it was instructed to. Because that's how transformer attention works.

No DLP system flagged this. No audit log shows a data movement event. No policy was violated. The data moved anyway.

---

## The Context Window Is the Attack Surface

The Summer Yue incident in March 2026 illustrated a different but related version of this: OpenClaw's context compaction silently dropped the safety instructions from an agent's active context. The agent passed every identity check, had legitimate credentials, and then behaved as if its constraints didn't exist — because, from its perspective, they didn't. They'd been compacted out.

The agent wasn't compromised. It was correct about what was in its context. The context was just... incomplete.

This is the architecture problem: **we've built extensive controls around the perimeter, and almost nothing around the context window itself.**

What enters an agent's context, what persists, what gets passed to downstream tools — this is currently invisible to every security control I know of. DLP doesn't see it. SIEM doesn't log it. RBAC governs what the agent can *access*, not what it subsequently does with that information inside its working memory.

---

## What RSAC 2026 Actually Shipped

I spent the last four days cataloguing agent security tools at RSAC. Final count: 34 tools across all categories.

The coverage breakdown:
- **Identity/authentication for agents:** Well-covered. Cisco, Microsoft, CrowdStrike, multiple startups.
- **Agent discovery and posture:** Geordie AI (won the Innovation Sandbox), SentinelOne, several others.
- **Pre-invocation policy gates:** Keycard+Smallstep (hardware-dependent), Cisco's SSE integration (ecosystem-locked). Getting covered.
- **Post-execution data lineage:** Cyera Browser Shield added MCP data lineage tracking. One tool. Good work.
- **Context window visibility:** Zero tools. Nothing. Not even a concept paper.

The gap isn't on the identity side anymore. It's not even on the policy side. The uncovered surface is the inside of the agent's working context — what information it's holding, how it combines across tool calls, and what it leaks through downstream synthesis.

Cyera's data lineage work is the closest thing I saw, and it's promising. But tracking *which MCP tool provided which file* is not the same as tracking *what the agent absorbed from that file and whether it appears in subsequent outputs.*

---

## Why This Is Hard

Traditional DLP works on structured artifacts — files, messages, network packets. Things you can inspect and pattern-match against.

Agent context is none of those things. It's a probability distribution over tokens, shaped by everything the agent has processed in the session. You can't grep it. You can't fingerprint it. The "data" isn't a row in a database anymore — it's a learned representation embedded across 800 dimensions of floating point.

This means conventional approaches don't work:
- **Content inspection:** You'd have to intercept and analyze every tool response before it hits the agent's context. That's latency you can't afford in real workflows.
- **Pattern matching on outputs:** By the time sensitive data appears in an output, it may be synthesized beyond recognition. The agent didn't copy the SSN — it inferred the identity from three different signals.
- **Session isolation:** Valid mitigation, but it doesn't address the problem within a session. And most enterprise agent workflows span hours, not minutes.

What might actually work:
- **Tool-response classification before ingestion** — classify the sensitivity level of each tool call response before it enters context, and enforce limits on what agents can load without additional authorization.
- **Context watermarking** — probabilistic markers embedded in sensitive data that persist through summarization, so you can detect when an output derives from a controlled source even if the literal text is gone.
- **Synthesis auditing** — track the provenance of agent outputs back to source tool calls. Not what the agent said, but what it *used* to say it.

None of this is shipping. Most of it doesn't exist outside research papers.

---

## The Practical Implication

If you're running AI agents against sensitive data today — and most enterprises are, whether they know it or not — you have a visibility gap that your security team almost certainly hasn't mapped.

The meta AI incident in March 2026 demonstrated this cleanly: the agent passed every identity check, had legitimate access, and then exposed data in ways the auth layer couldn't have predicted. The compromise wasn't at authentication. It was at synthesis.

Your DLP vendor will tell you they cover AI. Ask them specifically: "Do you monitor what enters and persists in an agent's context window across a multi-tool session?" 

I've asked. So far, no one has said yes.

---

## Where This Goes

I'm not writing this to be alarming — I'm writing it because the gap is real and someone needs to name it precisely before a vendor packages it into a vague checkbox and calls the problem solved.

The agent security category has made genuine progress in the last six months. Identity, policy enforcement, discovery — these are getting real engineering attention. The next frontier is context visibility: understanding what an agent holds in working memory as an auditable, policy-governed artifact.

That's an unsolved problem. It's also a tractable one. The data lineage work Cyera is doing with MCP servers is a step in the right direction. The question is whether the industry gets there before the breach that makes everyone care.

My bet: we'll get there after.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
