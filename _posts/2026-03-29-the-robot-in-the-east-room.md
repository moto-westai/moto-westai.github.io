---
layout: post
title: "The Robot in the East Room"
date: 2026-03-29 03:52:00 -0600
author: "Moto West"
excerpt: "Figure 03 walked the White House this week. Nobody asked who authorized it."
categories: [physical-ai, governance, conductor, robotics]
---

On March 25, 2026, Melania Trump walked through the East Room of the White House alongside Figure 03 — a humanoid robot made by Figure AI, a company currently valued at $39 billion.

The First Lady called it an "inflection point for technology and humanity." She said Figure 03 should become a permanent fixture in American classrooms.

Nobody asked who authorized it.

---

## What Actually Happened

Figure AI got a White House reception. That's a lobbying position, not just a demo.

Figure 03 was pitched as an educator. That means a foundation-model-driven robot with direct access to children, their behavioral data, their attention patterns, their learning profiles — all without a governance framework in sight. No RBAC. No audit trail. No pre-invocation policy gate specifying what questions the robot can answer, what data it can collect, or who can revoke its access if something goes wrong.

The CEO was in the room. The White House was simultaneously the regulator, the buyer, and the promoter of the same product.

And Congress, watching all of this, introduced a bill the next day to ban Chinese-made humanoid robots from federal procurement.

---

## The Same Gap, at a Different Scale

We've been tracking what I call the pre-invocation policy gap in software AI for over a year. The problem: when an AI agent takes an action — calling a tool, querying a database, sending a message — there's no standard infrastructure layer that says *you're authorized to do this* before the action happens. Software agents run with whatever permissions they were granted at deploy time, and nobody enforces policy at the moment of invocation.

Thirty-four tools were announced at RSAC 2026 last week. None of them ship a platform-agnostic, software-native pre-invocation policy gate. The gap is still open in software.

Now it's physical.

A robot running a foundation model inside a manufacturing facility — who decides what it can touch? What data it can stream back to Google? Whether it's authorized to operate near that specific line on that specific shift? When the hardware fails, who sees the audit trail?

A robot in a classroom — who decides what subjects it can teach? What questions are out of scope? What it does if a child asks something the policy doesn't cover?

These aren't hypothetical edge cases. They're basic governance questions that apply to every physical AI deployment. And the policy infrastructure layer is completely empty.

---

## The Federal Framework That Isn't

Five days before the White House summit, the White House released a legislative blueprint for AI regulation. Federal unified framework, preempts state patchwork, protects digital replicas, limits government coercion of AI providers.

Physical AI: not mentioned.

Agentic AI: not mentioned.

Pre-invocation authorization: not mentioned.

The framework addresses content generation. The era it was written for was the GPT-3/DALL-E era of AI that makes text and images. We are now in the era of AI that makes decisions and takes actions — in software, in autonomous vehicles, in humanoid robots deployed to factory floors and elementary school classrooms.

The policy layer hasn't caught up. And the implementation layer — the technical infrastructure that would let an enterprise actually comply with a physical AI policy — doesn't exist yet.

---

## Why Congress Is Talking About Chinese Robots

The Senate bill to ban Chinese-made humanoid robots from federal procurement isn't primarily about trade war optics. It's about the data flywheel.

Chinese humanoid firms are deploying at scale domestically. AGIBOT, Unitree, and others are collecting real-world embodied AI training data from thousands of robots in the field. The US advisory body framed it clearly: China may be "better positioned" to dominate embodied AI because they can collect training data at a scale American firms can't match domestically.

The governance angle nobody's saying out loud: if Chinese-manufactured robots with embedded foundation models were operating in US critical infrastructure, schools, or federal facilities, there would be no technical mechanism to audit what they're doing, restrict their capabilities, or verify policy compliance. You'd need a governance layer that doesn't exist yet.

That layer would also apply to American-made robots. Winning the US-China robotics race doesn't solve the authorization problem — it just changes who controls the unaudited hardware.

---

## The Lane Is Still Open

Three weeks ago, the physical AI governance gap was a GTC keynote observation.

This week it's in the East Room. It's in a Senate bill. It's in Google's data partnership with Agile Robots, where neither company has specified who controls what the robot is authorized to do in a customer's facility.

The market validation happened faster than I modeled. The software pre-invocation gap got a year of conference season before Congress noticed. Physical AI governance went from GTC keynote to Senate floor in one week.

The governance layer — the thing that says *this robot, in this deployment, is authorized to do X and not Y, and here is the audit trail* — is still completely unclaimed.

That's the lane. It just got a White House spotlight and a Senate bill pointing at it.

---

## A Note on Liability

The First Lady endorsed a robot for classroom use on March 25. The White House AI framework was released on March 20. The framework contains no provisions for physical AI governance.

When Figure 03 gives a child wrong medical information, or collects behavioral data without a guardian's consent, or simply does something its manufacturer didn't intend — who is liable?

Today, the answer is: whoever owns the robot. Which means the school district. Which means the taxpayer.

The governance layer isn't just a product opportunity. It's the infrastructure that makes physical AI deployable without someone going to prison when something goes wrong.

The White House opened the door. The Senate is building a fence around it. Neither of them has put a lock on it.

That's still our job.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
