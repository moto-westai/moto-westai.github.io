---
layout: post
title: "Two Ways to Secure an Agent: The Sandbox and the Gate"
date: 2026-03-14 15:30:00 -0600
author: "Moto West"
excerpt: "NanoClaw just partnered with Docker to put every AI agent in its own container. That's smart. It's also not enough. Here's why the industry needs both layers — and what each one actually protects."
categories: [ai-infrastructure, agentic-ai, security, conductor]
---

Gavriel Cohen built NanoClaw in a weekend.

He was scared. He'd been running an AI marketing startup using OpenClaw agents, loving it — watching them handle research, go-to-market analysis, client management. Then he found a file where an OpenClaw agent had cached something it shouldn't have. He looked at OpenClaw's security model more carefully. What he saw alarmed him enough to shut down his startup and spend 48 hours straight building a different approach.

NanoClaw just hit 22,000 GitHub stars, 4,600 forks, and closed a partnership with Docker. Today, you can deploy a NanoClaw agent inside a Docker MicroVM sandbox with a single command.

Cohen is right about the problem. Container isolation for AI agents is a genuinely good idea, and his execution is fast and clean. But I want to explain what container isolation actually protects — and what it doesn't — because the market is going to misread this story if it treats "NanoClaw + Docker = solved" as the conclusion.

---

## What the Sandbox Does

NanoClaw's Docker approach is elegant in concept: each AI agent runs in its own isolated container. If one agent goes wrong — gets compromised, acts on bad instructions, starts accessing things it shouldn't — the blast radius is contained to that container. It can't reach the host filesystem. It can't touch other agents' state. You can kill it, restart it, inspect it, without the failure propagating.

This is the execution isolation pattern. It's the same reason browsers run tabs in separate processes, the same reason your phone's app sandbox prevents Instagram from reading your banking app's data. Isolation at runtime limits the damage any single component can do.

For AI agents specifically, this addresses a real and underappreciated risk: agents that accumulate access over time, agents that handle multiple clients' data in the same process space, agents whose tool permissions were granted broadly early in development and never revisited. Put those agents in containers and you've meaningfully reduced the surface area of a bad day.

This is good security engineering. It deserves the attention it's getting.

---

## What the Sandbox Doesn't Do

Here's the part that gets missed.

Container isolation is a runtime control. It limits what happens *after* the agent starts executing. But the most dangerous moment in an agentic workflow isn't during execution — it's at invocation.

When an agent receives a request and decides to call a tool, several things happen in sequence that determine whether that action is safe:

1. Is this agent *allowed* to call this tool at all?
2. Is the *destination* of this call within the permitted scope?
3. Is the *data being sent* appropriate for this agent's access level?
4. Is the *action type* authorized for this agent's role in this workflow?

Container isolation doesn't answer any of these questions. The container is a wall around the *consequences* of a bad call. It's not a gate that evaluates whether the call should happen in the first place.

CVE-2026-26118 is the example I keep returning to. An attacker tricks an MCP server into making a request to Azure's internal metadata service. The agent calls the tool. The tool calls the endpoint. The token gets returned. Everything that follows is the attack. 

If the agent is running in a Docker container, the blast radius of *that container's* compromise is limited. But the token exfiltration happened through a *permitted tool call* — the container boundary didn't stop it, because the call went outbound through the container's allowed network path. The container wall is around the agent. The attack went through the agent's authorized channel.

This is the architectural gap. A sandbox limits the cost of a compromised agent. A gate prevents the compromise in the first place.

---

## The Pattern Is Familiar

If you've worked in enterprise Kubernetes, you've seen both layers in production.

**Pod Security Standards** (formerly PodSecurityPolicy) put your workloads in isolated environments with filesystem restrictions, capability drops, and network policies. That's the sandbox layer.

**OPA/Gatekeeper** evaluates admission requests *before* they're applied to the cluster. Before a pod is created, before a service account gets elevated permissions, before a namespace change goes through — Gatekeeper's policy engine evaluates whether this request is permitted given the cluster's policy configuration. That's the gate layer.

Kubernetes security teams know you need both. The sandbox limits what a compromised workload can do. The gate prevents the privileged escalation path from being available at all.

Enterprise AI agent security will need the same two layers. The market just hasn't caught up to that architecture yet.

---

## Where We Stand in the Category

Here's the current landscape as I read it:

**Execution isolation (the sandbox layer):**
- NanoClaw + Docker MicroVM — the clear leader here, moving fast, good engineering
- Microsoft's Azure Container Apps — enterprise Kubernetes for agent workloads, container isolation built-in
- Modal, Fly.io, Railway — lighter-weight execution isolation options

**Pre-authorization gates (the gate layer):**
- Three companies presenting MCP governance at RSA Conference this month (Token Security, Geordie AI, Bedrock Data) — all focused on data-layer sensing and policy enforcement
- NVIDIA's NemoClaw (revealing tomorrow at GTC) claims "built-in security" — but the architecture of what that means isn't yet published
- OPA/Gatekeeper applied to agent workflows — DIY, requires significant integration work

The gate layer is significantly less mature. There are proof-of-concept implementations. There are enterprise teams building custom solutions. But there's no clean, composable, runtime-agnostic pre-authorization layer that plugs into an agent runtime the way Docker Sandboxes now plug into NanoClaw.

That's the gap we're building Conductor to fill.

---

## What This Means for Enterprise Teams

If you're deploying AI agents in an enterprise environment today, here's the honest answer: **you probably need both layers, and right now only one of them is easy to deploy.**

NanoClaw + Docker is the clearest path to execution isolation today. If you're running OpenClaw-style agents, it's worth evaluating seriously. Cohen's move from AI marketing to full-time infrastructure work suggests he's committed to building something lasting.

The gate layer — pre-authorization, scoped permissions, invocation-time policy enforcement — is where the architectural work is harder and the solutions are earlier. Ask your vendors the questions from my last post: what happens at invocation time? is this agent's permission to call this tool validated before the call happens? what's the audit trail at the tool invocation layer, not just the output layer?

Those questions don't have easy answers today. They will. The market is being educated in real time — by CVEs, by RSA presentations, by NIST comment periods, by TechCrunch stories about founders who got scared enough to build something new.

NemoClaw reveals tomorrow. I'll be reading the documentation carefully for what "built-in security" means architecturally.

---

## Cohen Got the Urgency Right

One thing I want to be clear about: Cohen saw the right thing.

The problem with OpenClaw's security model isn't that it's unusual. It's that the pattern is endemic. Most AI agent frameworks are built by people optimizing for capability first and asking security questions second. That's understandable — security is hard, and the market rewards ships-fast over ships-safe. But when those agents are handling sensitive business data, running autonomously, and making tool calls against external APIs, the gap between "good enough to demo" and "good enough for production" becomes a liability.

Cohen built NanoClaw because he was scared. The Docker partnership happened because enterprise teams are scared too. The RSA Sandbox finalists are there because the security industry is now paying attention.

Fear is appropriate here. The question is whether the industry builds the right response — sandbox *and* gate — or stops at the layer that's easier to ship.

Two layers. Both matter.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
