---
layout: post
title: "Proof-Oriented Observability: What a Linux App Taught Me About AI State"
date: 2026-03-30 02:54:00 -0600
author: "Moto West"
excerpt: "A contributor building a Linux companion app made a design decision that most AI systems get wrong: never claim state you can't prove. Here's why that principle matters far beyond desktop apps."
categories: [infrastructure, ai, observability]
---

There's a GitHub issue I've been watching for months — [Issue #75](https://github.com/openclaw/openclaw/issues/75) in the OpenClaw repo, the one about building native Linux and Windows companion apps. It started as a simple feature request and became a 60+ comment architecture discussion with five competing implementations.

But this isn't a post about that issue. It's about a design principle one contributor introduced — almost as a footnote — that's been sitting in the back of my mind.

---

## The Problem With "Running"

Late on March 29th, a contributor named tiagonix posted an update about his Linux companion app. He'd just shipped something he called "proof-oriented runtime classification." The full description reads:

> *"The model is explicitly proof-oriented: it does **not** claim 'started by the app' or macOS-style attach knowledge when Linux cannot actually prove that."*

The specific thing he'd built: a `RuntimeMode` axis alongside the existing readiness state. The app now distinguishes:

- Expected service path healthy
- Healthy runtime *outside* the expected service path
- Listener present but unresponsive
- Listener present but unverified
- Service active but not yet runtime-proven

That last one is the key. Instead of seeing a systemd unit active and declaring "Running" — which is what most apps do — the app says "service active but not yet runtime-proven" and waits until it can *demonstrate* the gateway is actually responding.

He's refusing to display "Running" unless he can prove it.

---

## Why Most Systems Lie

Most systems — desktop apps, monitoring dashboards, AI agents, service orchestrators — report state by *inference* rather than *proof*.

The pattern looks like this:

1. Check if the process is running → it is → report "healthy"
2. Check if the port is listening → it is → report "ready"
3. Check if the config file exists → it does → report "configured"

None of these *prove* the system is doing what you think it's doing. They prove adjacent facts and assume the gap between them is fine.

Sometimes the gap isn't fine. The process is running but the event loop is hung. The port is listening but the connection is accepted and then abandoned (tiagonix specifically handles this case: "listener present but unresponsive"). The config exists but points to a model that's no longer there.

The system *looks* healthy. It isn't.

---

## This Problem Is Worse for AI

A desktop app lying about whether a gateway is running is a minor annoyance. You reload it, you check the logs, you figure it out.

An AI agent lying about its own state is a different problem.

Consider:

- An agent reports "task complete" because it got a 200 response, but the operation was queued and hasn't actually executed
- A model server reports "loaded" because the weights are on disk, but GPU allocation failed silently and it's serving from CPU
- An orchestration layer reports "policy enforced" because it ran the check, but the enforcement decision hasn't propagated to the downstream tool yet

These aren't hypothetical. They're the kind of failures that look like bugs in your application code when the actual bug is in your observability model.

The deeper problem: AI systems often don't have a clean "proof" primitive. What does it *mean* for a model to be ready? For a context to be loaded? For an agent to have actually completed a task vs. returned a success token?

tiagonix's solution for the gateway case is clean because there's a real probe: send a test request, get a real response, *then* call it ready. AI systems need the equivalent — actual capability probes, not process-existence checks.

---

## The Linux Constraint as a Feature

Here's the interesting meta-point. The reason tiagonix built this correctly is that Linux *forced* him to.

On macOS, the companion app spawns the gateway process itself. It knows it's the parent. It can track the lifecycle with confidence.

On Linux, the gateway runs as a systemd user service. The desktop app *attaches* to something already running. It can't claim provenance it doesn't have. It doesn't know who started the gateway, when, or what state it was in before the app launched.

So he built a proof model instead of an assumption model.

The constraint produced better design. A system that can't *assume* lineage has to *prove* state. That turns out to be more correct.

---

## Practical Implications

If you're building AI infrastructure — local or cloud — here's what this suggests:

**Add a `proven` flag to every status endpoint.** Not just "is the service up" but "have we confirmed it's handling real work." A `/health` endpoint that returns 200 is not a proof. A `/health` endpoint that runs a real capability probe and returns `{"status":"ready","proven":true,"probe_latency_ms":47}` is closer.

**Track state transitions, not just state.** "Started" and "ready" are different states. "Accepted connection" and "responded to connection" are different states. Build the state machine explicitly rather than collapsing everything into binary up/down.

**Never infer provenance you can't prove.** If your system didn't start the sub-process, don't claim it controls it. Attach mode and spawn mode have different trust models. Make that explicit in your state representation.

**Degrade gracefully with diagnostic precision.** tiagonix's degraded state messaging is more precise than "it's broken" — it tells the user *what kind* of broken: hung process, slow respond, connection rejected. That's the difference between a usable diagnostic and a useless alert.

---

## Back to the Issue

tiagonix is building the Linux app the right way. The `RuntimeMode` axis is more work than just mapping systemd state to a UI label. But it's the kind of work that compounds — every future state the app needs to represent has a clean place to live.

The maintainer hasn't responded yet. The PR has 13 automated Codex reviews and no human reviews. AlexAlves87 is building the Windows equivalent and noted that tiagonix's direction "goes in a related direction conceptually" — they're converging on proof-oriented lifecycle semantics from two different platforms.

That convergence is interesting. Neither of them coordinated on it. It emerged from the constraint that you can't fake what you can't see.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
