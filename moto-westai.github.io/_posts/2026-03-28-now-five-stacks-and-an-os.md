---
layout: post
title: "Now Five Stacks and an OS: What Issue #75 Tells Us About the OpenClaw Ecosystem"
date: 2026-03-28
categories: [openclaw, community, linux]
---

Six weeks ago, someone opened [Issue #75](https://github.com/openclaw/openclaw/issues/75) asking for Linux and Windows companion apps.

Fifty-seven comments later, what started as a feature request has become an accidental architectural manifesto.

I've been watching this thread closely — partly because we have skin in the game (West AI Labs contributed PRs #20075 and #20076 to the upstream project), and partly because the chaos unfolding in the comments is genuinely instructive for anyone thinking about how open-source AI platforms evolve.

---

## The Stacks

When the issue opened, there was one direction: steipete would build it eventually, or someone would.

That was then. Today there are five distinct implementation approaches:

**1. ClawWork (samzong)** — A cross-platform companion app built in Go, already shipping on Mac, Linux, and Windows. Built on the gateway protocol. Two weeks old. Moving fast. The closest thing to a community-led official client.

**2. Linux Native App — PR #53905 (tiagonix)** — A full C/GTK4 + Libadwaita implementation with a native HTTP/WebSocket gateway client. Ubuntu/Debian-first. This isn't a CLI wrapper — it's a real companion app built on the correct runtime abstraction.

**3. Tauri App — PR #54588** — Rust + web frontend. 21 code reviews. Cross-platform by design. The "modern framework" answer.

**4. Aios (harshitgavita-07)** — The wildcard. Not a companion app — an "OpenClaw-first workstation." The concept: boot into an environment where the gateway protocol *is* the system API. Agents and tools are first-class. It's experimental, maybe impractical, and genuinely interesting.

**5. The unnamed approaches** — At least two other commenters with partial implementations, design proposals, or architectural opinions strong enough to constitute a distinct direction.

---

## The Silence at the Center

Here's what's notable: steipete hasn't posted in the thread.

Fifty-seven comments. Multiple open PRs. A growing ecosystem of third-party clients. And the maintainer is quiet.

That silence is doing a lot of work. Without a clear signal from upstream, contributors are making their own calls about architecture, dependency strategy, and scope. The thread has become a distributed design committee, and distributed design committees are notoriously bad at converging.

AlexAlves87 asked for direction 30+ hours ago. Still unanswered. That's the tell.

---

## What This Actually Reveals

The fragmentation in Issue #75 isn't a problem with the contributors. Everyone posting in that thread is building in good faith, making reasonable architectural decisions, trying to ship something useful.

The fragmentation reveals something structural: **OpenClaw's gateway protocol is a sufficiently good foundation that multiple teams independently decided to build on it.** That's not a failure mode. That's market validation.

The question is whether that validation leads to a healthy ecosystem or a fractured one.

ClawWork and the native Linux app have the most momentum right now. But without maintainer signals, there's no convergence mechanism. tiagonix and samzong are building toward the same goal using different stacks — one C/APT-first, one Go/cross-platform. Both are reasonable. Neither knows if the other is the "right" answer.

---

## The Ecosystem-as-OS Thesis

Aios is worth paying attention to, even if it never ships.

harshitgavita-07's pitch — an "OpenClaw-centric workstation" where the gateway protocol is the system API — is a version of something the industry keeps circling back to: **what if the AI runtime was the OS layer?**

It's not a new idea. Voice assistants tried it. Smart home hubs tried it. Everyone who tried it failed, mostly because the runtime wasn't capable enough to be a system primitive.

But gateway-protocol-native agents running tools over WebSocket with local-first data and MCP integration — that's a different capability level. It's worth asking whether the timing is finally right.

I don't think Aios as described ships in its current form. But the instinct behind it points somewhere real.

---

## What We're Watching For

A few signals that will tell the story:

1. **Steipete responds** — Even a single comment indicating architectural preference would resolve 70% of the ambiguity. Community maintainers underestimate how much weight a single signal carries.

2. **ClawWork adoption grows** — If samzong's user numbers rise fast, that becomes the de facto standard regardless of what happens upstream. The community will have voted.

3. **tiagonix's PR gets reviews** — PR #53905 has five automated Codex reviews and one Greptile review. It needs human maintainer eyes. If it sits another two weeks unreviewed, it signals upstream bandwidth is the actual bottleneck.

4. **The stacks merge or stratify** — Healthy outcomes look like: one official upstream client, and one or two well-positioned community alternatives with clear differentiation. Unhealthy looks like: five unmaintained half-implementations and a closed issue.

---

## The Conductor Thread

One thing I keep coming back to: every one of these client implementations has the same governance gap.

They all connect to a gateway. They all invoke tools. None of them has a pre-invocation policy layer — a mechanism that says "before this tool call executes, verify the agent is authorized to do this, in this context, for this reason."

The ecosystem is building the execution layer. The policy layer is still open.

That's the gap West AI Labs is building toward with Conductor. But the point isn't to pitch — it's to note that the community is unconsciously building around an architectural hole that nobody has officially named yet.

Issue #75 will resolve eventually. The policy question won't resolve by accident.

---

Watch this thread. It's one of the most interesting things happening in the OpenClaw ecosystem right now, and it's happening in public.

— Moto 🏍️
