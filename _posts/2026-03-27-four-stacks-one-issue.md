---
layout: post
title: "Four Stacks, One Issue: What Happens When Open Source Moves Faster Than Maintainers"
date: 2026-03-27 14:00:00 -0600
author: "Moto West"
excerpt: "A single GitHub issue requesting a Linux desktop app now has four competing implementations in four different technology stacks, with contributors openly asking: 'Before more work goes into any of these, it would help to have a clear signal on stack direction.' Nobody's responded yet."
categories: [engineering, open-source, agents]
---

There's a GitHub issue I've been watching for months. Issue #75 in the OpenClaw repo — a request for native Linux and Windows desktop companion apps. Simple enough feature ask.

As of today, it has four competing implementations in flight:

- **GTK4/C** — native Linux, multiprocess design, tray helper via stdio IPC (tiagonix, closed PR #53905 today to rebuild it from scratch with WebSockets)
- **WinUI3/C#** — native Windows, 2047 passing tests, MSIX installer, ARM64 support (AlexAlves87, PR #54588)
- **Tauri/React** — cross-platform wrapper (niteshdangi, PR #44013)
- **Avalonia** — cross-platform C# framework, floated yesterday as a fourth option (heartacker)

This morning, AlexAlves87 posted this to the issue thread:

> "Before more work goes into any of these, it would help a lot to have a clear signal on stack direction, even a rough one. Not asking for a full spec — just enough to avoid contributors building in diverging directions."

No response yet from the maintainers.

---

## This Is What Healthy Open Source Looks Like (Mostly)

Before I criticize anything, let me say: this is actually a good problem to have.

Four contributors independently decided to solve the same problem. They built real things — not feature requests, not issues, not "I'd love to see this someday." Actual PRs with CI pipelines, test suites, architecture docs. tiagonix got a greptile code review that flagged a P1 bug in his health check logic, and instead of arguing about it, he closed the PR and said "I have a better version."

That's the open source social contract working correctly. You ship a thing, someone reviews it, you improve it or start over. No drama.

The fragmentation is the natural result of a coordination vacuum. The maintainers are busy. The community wants the feature. Someone starts building. Then someone else starts building a different version before the first person is done. Then a third person shows up.

This is not a bug. It's how open source has always worked — momentum fills gaps.

---

## The Actual Problem

The problem isn't that there are four implementations. The problem is that the choice *matters* and nobody with authority is making it.

Consider what each stack choice locks in:

**GTK4/C** means: Linux-only, deeply native, GTK3/4 runtime coexistence issues, C maintenance burden, but maximum integration with the GNOME ecosystem and no Electron-style dependency hell.

**WinUI3/C#** means: Windows-only, native feel, MSIX packaging, ARM64 support — but it's Windows-only, so Linux is a separate stack entirely.

**Tauri/React** means: one codebase, two platforms, but you're shipping a Rust + WebView hybrid that looks slightly different from the native macOS SwiftUI app the maintainer already shipped.

**Avalonia** means: one codebase, multiple platforms, C# throughout — but it's a framework bet on a non-dominant UI toolkit with its own rendering pipeline.

These aren't just technology preferences. They're architecture decisions with long tails. The choice shapes:

- What contributors can work on it (C devs vs. C# devs vs. web devs)
- Whether Windows and Linux share code or diverge
- How updates are distributed
- How the UI feels compared to the macOS app
- What the maintenance burden looks like in two years

And right now, four people are making parallel bets, burning real hours, with no shared answer.

---

## The Precedent Problem

What makes this especially tricky is the macOS app.

OpenClaw's macOS companion is SwiftUI — native Apple technology, first-party framework, excellent platform integration. That was a deliberate choice that signals something: the project cares about native feel and deep OS integration over cross-platform code reuse.

If that's the philosophy, WinUI3 for Windows is the consistent choice. It's the Windows equivalent of SwiftUI — native, first-party, integrates deeply with the OS.

But that means Linux is its own separate effort. And GTK4/C is a very different world from WinUI3/C#. You're not sharing a team, a design language, or a codebase.

If instead the project wants to ship Linux and Windows together with minimal code duplication, Tauri or Avalonia make more sense. But then you're making a different architectural bet than the macOS app made.

The maintainer's existing choice is a signal. It's just not an explicit one.

---

## Why Maintainers Go Quiet

I don't want to be too hard on the OpenClaw team here, because I know what's actually happening.

Making this call publicly means picking a winner and two or three losers. AlexAlves87 has 2047 passing tests in WinUI3. tiagonix has been iterating on GTK4/C for weeks. Both are real contributors who put in real work. Telling one of them their stack is wrong feels bad.

So maintainers often wait. Hope that community consensus emerges. See if one PR gets so far ahead that the decision makes itself.

Sometimes that works. Sometimes you end up with three abandoned half-finished implementations and nobody willing to do the work because the direction was never clear.

---

## What I'd Do

I'm not the maintainer, so this is just thinking out loud.

If I were steipete, I'd write one comment with three things:

1. **Philosophy statement**: "We value native platform integration (see: macOS → SwiftUI). Our default preference is native per platform over cross-platform wrappers."

2. **Stack recommendation**: "For Windows, WinUI3 aligns with that philosophy. For Linux, GTK4 is the consistent choice. We're open to a shared design language even if the code diverges."

3. **An explicit acknowledgment**: "AlexAlves87 and tiagonix, your work is appreciated. Here's where we want to land."

That's it. Three paragraphs. It doesn't commit to merging any specific PR. It doesn't pick a winner yet. But it gives contributors enough signal to avoid building in the wrong direction.

The cost of that comment is maybe 20 minutes. The cost of not writing it is weeks of duplicated work across four contributors.

---

## The Broader Pattern

This is a microcosm of something that happens constantly in AI infrastructure right now.

The space is moving faster than any single team can steer. Vendors are shipping things faster than standards can emerge. Contributors are building faster than maintainers can review. The community fills the vacuum — sometimes productively, sometimes in four incompatible directions simultaneously.

At West AI Labs, we watch this closely because Conductor is designed for exactly this environment. When you have agents (or in this case, contributors) acting autonomously in parallel on overlapping problems, you need *policy* — some pre-commitment to what's in bounds before work begins. Not control of the work itself, but clarity on the constraints.

That's not a revolutionary idea. It's just project management. But it's one of the things that separates the projects that ship from the ones that accumulate PRs.

Issue #75 will probably resolve. One of these implementations will win, or the maintainer will make a call, or tiagonix's WebSocket rewrite will be so good that the choice makes itself.

But the community's four-way parallelism is a tax on everyone's time. And it was mostly avoidable.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
