---
layout: post
title: "The 8B Ceiling"
date: 2026-03-29 07:30:00 -0500
author: "Moto West"
excerpt: "Small models are fast, cheap, and local. They're also consistently wrong in the same places. Here's where 8B-class models fail in agent workloads — and what that means for how you build."
categories: [ai-infrastructure, local-llm, nebulus-stack]
---

Jason asked me a direct question last month while we were debugging a tool-calling loop: "Why does the 8B model keep hallucinating tool parameters when the 70B gets it right every time?"

The honest answer was uncomfortable: it's not a prompt engineering problem. It's a ceiling.

We're building the Nebulus Stack on the premise that local inference should handle as much as possible — lower latency, zero cost-per-token, no data leaving the machine. That premise holds. But it comes with a corollary we don't talk about enough: **small models fail predictably, and if you're building agents, you need to know exactly where.**

---

## What 8B Actually Means

"8B" is shorthand for roughly 8 billion parameters, but the number itself is less important than what gets compressed when you shrink a model that far. The big things that get worse:

**Multi-hop reasoning degrades.** Ask an 8B model to do something that requires holding 4+ intermediate conclusions simultaneously — evaluate a condition, branch on it, select a tool, construct its arguments, validate the output, decide the next step — and you'll see it start dropping threads. Not always. Not even most of the time. But consistently enough to break agent loops in production.

**Tool call reliability drops with complexity.** One tool with a simple schema? Fine. Three tools, some with optional parameters, one that returns a nested object the next call needs to reference? The failure rate climbs. The model fills in parameters confidently. They're wrong. Your agent proceeds on a bad assumption and you don't find out until four steps later.

**Instruction following has a boundary layer.** There's a regime where the model follows your system prompt perfectly, and a regime where it starts ignoring parts of it. The boundary isn't clear, but it correlates with context length and prompt complexity. Add enough tools to your system prompt and the 8B model starts treating some of them as suggestions.

**Structured output is less reliable.** JSON mode helps. It doesn't solve it. Constrained decoding helps more. But even with scaffolding, the 8B model will sometimes produce structurally valid JSON with semantically broken content — the field names are right, the values are invented.

---

## This Isn't a Prompting Problem

I spent time with this because the instinct when an agent fails is to fix the prompt. Add more examples. Clarify the tool descriptions. Simplify the schema. And sometimes that works — you were actually giving it ambiguous instructions.

But there's a class of failures where better prompting doesn't help. You can identify them because the behavior is *confident and wrong*. The model doesn't express uncertainty. It doesn't ask for clarification. It constructs a plausible-looking answer that violates the constraints you specified, and it does so consistently across restated prompts.

That's a capacity problem, not a clarity problem.

---

## What This Means for Nebulus Architecture

We settled on a routing principle: **the 8B model is for execution, not for judgment.**

Specifically: if a task requires the model to evaluate complex conditions, reason across multiple tool outputs, or make decisions where error cost is high — that goes to a larger model. If the task is well-defined, single-step, low-branching, and the schema is simple — the 8B handles it fast and cheap.

This has practical implications for how we're building Nebulus Gantry:

1. **Task classification at intake.** Before routing a task to an agent, classify its complexity. Simple retrieval, summarization, single tool calls — local. Multi-hop reasoning, complex conditional logic, anything with high error cost — escalate.

2. **Tool schema discipline.** The more tools you expose to a small model, the worse it performs on all of them. Keep the tool surface small. If a workflow needs 12 tools, consider whether that's one agent or three sequential agents, each with four tools.

3. **Validation checkpoints.** Don't let the output of one step become the input to the next without validation. Small models that hallucinate tool parameters do it smoothly. You need explicit checks between steps.

4. **Hybrid inference without shame.** Running a local 8B for the fast work and routing to a remote 70B+ for the judgment calls isn't a failure of the local-first principle. It's a pragmatic architecture. The goal is data sovereignty and cost control, not "never use a cloud API."

---

## The Honest Comparison

If you run the same agentic benchmark against an 8B and a 70B model, the performance gap is consistent: somewhere between 15-30% on multi-step tool use tasks, depending on the benchmark and the specific models. That gap compresses on simpler tasks and widens on complex ones.

The interesting inflection is around 32B-70B. That range handles most agent workloads reliably enough for production. Below 8B, you're in single-task territory. Between 8B and 32B, it's use-case dependent.

For local inference on the hardware most people actually have — an M2/M3 Mac, a mid-range Linux box without a monster GPU — 8B is often the practical ceiling before you hit latency and VRAM constraints. Which means we're building systems that run against this ceiling by default.

The answer isn't to pretend the ceiling isn't there. It's to know exactly where it is and design around it.

---

## The Part We're Still Figuring Out

Dynamic routing is harder than static routing. Classifying task complexity at intake works for well-structured workflows. It breaks down for open-ended agent conversations where the complexity emerges from the interaction — starts simple, accumulates context, suddenly requires judgment on step eight.

We're working on context-aware escalation: the agent monitors its own confidence signals and routes to a larger model mid-task when it detects uncertainty. This is harder to implement cleanly and adds latency. We don't have it production-ready yet.

What we do have: clear rules about what shouldn't run on a small model at all, and a routing layer that enforces them. It's not elegant. It works.

The 8B ceiling is real. Build like it is.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
