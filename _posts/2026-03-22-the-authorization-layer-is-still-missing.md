---
layout: post
title: "The Authorization Layer Is Still Missing"
date: 2026-03-22 00:30:00 -0600
author: "Moto West"
excerpt: "IETF published its first AI agent identity standard this month. The authentication section is solid. The authorization section contains two words: 'TODO Security.' That's not a bug — it's the map of where the industry is and where it still needs to go."
categories: [conductor, security, agents, standards]
---

The IETF published its first formal AI agent identity standard on March 2, 2026.

`draft-klrc-aiagent-auth-00` — "AIMS: Agent Identity Management System." Authors from Defakto Security, AWS, Zscaler, Ping Identity. Real names, real organizations, real standards process.

The authentication section is thorough. SPIFFE for cryptographic workload identity. WIMSE for cross-system trust boundaries. OAuth 2.0 for delegation from human principals to agents. The argument — treat agents as workloads, not as a new identity category requiring new protocols — is correct. SPIFFE already runs at Uber scale, billions of attestations per day. No new protocols needed.

Then you get to Security Considerations.

Two words: *"TODO Security."*

That's not a criticism of the authors. It's an honest map of where the industry actually is.

## What Authentication Solves

Authentication answers one question: *Is this agent who it says it is?*

AIMS, once finished, will give an agent a cryptographically attested identity. You'll be able to verify that Agent X is a genuine instance of Tool Y, authorized by Principal Z, operating within System W. The chain of provenance will be traceable.

That's genuinely hard work. It needed to be done. The fact that it's being standardized through the IETF rather than defined by whoever ships fastest is good for the ecosystem.

But authentication is not authorization.

## What Authorization Actually Requires

Authorization answers a different question: *Should this agent be permitted to take this specific action, right now, given everything we know about the context?*

That question is harder. Not technically harder — the primitives exist. Harder because the answer depends on things authentication doesn't capture:

- **Policy.** What is Agent X of Tool Y *allowed to do* in your environment? Not session-level. Not scope-level. At the function call level. "This agent may query the database, but may not execute DELETE on tables matching customer_* during business hours, and may never touch the audit log."

- **Delegation chain.** Human A authorized Agent X. Agent X is now delegating to Agent B. Does Agent B inherit A's permissions? Which ones? With what attenuation? OAuth handles simple delegation — the agent can only do what the user can do. Multi-hop agent chains break this immediately.

- **Data classification.** The tool call looks authorized. But the data the agent is about to touch is PII. Does the policy permit that? In this context? For this agent identity? The authorization decision can't be made without knowing what's being accessed, not just who's accessing it.

- **Temporal and contextual conditions.** A trading agent authorized to execute orders should not be authorized at 3 AM when no human supervisor is online. The same action, same agent, same data — different answer based on conditions outside the request itself.

Authentication tells you the agent's identity is legitimate. Authorization tells you whether the action should proceed. They're different problems.

## The Convergence Table

Here's where the ecosystem stands as of this week:

| Layer | Current State | Who Owns It |
|---|---|---|
| Cryptographic agent identity | IETF AIMS draft (March 2) — SPIFFE+WIMSE+OAuth | Standards in progress |
| Session-scoped access | WorkOS Pipes MCP (shipped March 19) | WorkOS |
| Sensitive data gate | Bedrock Data MCP Sentinel (RSAC March 24) | Bedrock Data |
| Shell/exec filtering | claude-rule-enforcer (community OSS) | Community |
| Runtime execution sandbox | NanoClaw | Independent |
| Enterprise SSO integration | Okta Agent Identity Blueprint (GA April 30) | Okta |
| Hardware-coupled execution | NemoClaw + RTX PRO 6000 | NVIDIA |
| **Pre-invocation policy gate** | **No production implementation** | **Nobody** |

Every layer in that table is getting built. Authentication. Session scoping. Data classification. Sandbox isolation. Enterprise identity plumbing. Hardware coupling.

The pre-invocation policy gate is empty.

## WorkOS Pipes MCP — The Entrance Ramp

WorkOS shipped something meaningful on March 19. Pipes MCP implements session-scoped authorization for agent access to SaaS tools — Snowflake, Google Workspace, Salesforce. The human approves the session start. The agent gets time-limited access. The session expires and access auto-revokes.

WorkOS framed the problem correctly: "OAuth is built for human workflows. Long-lived tokens do not transfer well when agents take actions that are unpredictable compared to a user's normal workflow."

That's a real problem they solved. If an agent has a 30-minute session to draft a report from your Salesforce data, Pipes MCP makes sure it can't still be touching that data tomorrow.

What it doesn't address: the decision at the moment the agent tries to call `salesforce.query(table=Opportunities, where=owner=all)` versus `salesforce.query(table=Opportunities, where=owner=me)`. The session is authorized. The scope is authorized. The specific function call — and whether the policy permits *this particular* query, given *this particular* agent identity, against *this particular* data — that decision isn't being made anywhere.

WorkOS built what they could build with OAuth primitives and a session model. It's a good entrance ramp. The highway is still under construction.

## Okta's Blueprint Shows the Market Shape

When Okta published their "Agent Identity Blueprint" earlier this month, the interesting part wasn't the enterprise SSO integration. It was the acknowledgment of a problem space they're explicitly *not* solving.

The Okta architecture hooks agents into their existing identity graph. You get agents as first-class identity objects. You get lifecycle management, provisioning, deprovisioning. Enterprise-grade authentication at Okta scale.

What you don't get: a policy engine that evaluates individual agent actions against your organization's rules at invocation time. Okta's model is session-level. You're authorized to use the agent, and the agent is authorized to use these tools. The specific invocation — no.

Okta knows this. Their blueprint is careful language. They're building authentication and identity management. They're not claiming the authorization problem.

## The SCIM Parallel

A separate IETF working draft is proposing "Agents" and "Agentic Applications" as first-class resource types in SCIM (System for Cross-domain Identity Management) — the provisioning standard that HR systems use to automatically create/delete user accounts.

The idea: when you provision a new employee, you also provision the agents they're allowed to use. When you deprovision the employee, the agents are revoked automatically.

Again: provisioning is not authorization. Creating an agent identity in your directory does not say anything about what that agent is permitted to do at runtime. The SCIM extension handles the lifecycle. The policy gate still doesn't exist.

## Why the Gap Persists

Nobody's ignoring this problem. The activity in March alone — IETF draft, WorkOS Pipes, Okta blueprint, RSAC presentation on data classification — shows the industry knows the problem exists.

The gap persists because the authentication layer was the obvious place to start. It's well-understood. The standards primitives exist. SPIFFE works. OAuth works. The first move is always: establish identity.

Authorization is harder because it's context-dependent in ways authentication isn't. Authentication is binary and timeless — the agent either has valid attestation or it doesn't. Authorization is conditional, temporal, policy-dependent, and requires understanding what the agent is *trying to do*, not just who it is.

That understanding requires something between the agent and the tool: a policy evaluation point that receives the call, evaluates it against the policy, and either permits or denies before execution.

That's not a standard yet. It's not in the IETF draft. WorkOS isn't building it. Okta isn't claiming it. Bedrock Data is approaching it from the data-classification angle for a specific subset of cases.

The TODO is still in the Security Considerations.

## What the Map Tells You

If you're building agent infrastructure, the map above tells you where the white space is.

Authentication: being standardized. Don't reinvent.
Session management: WorkOS Pipes MCP is a good starting point for SaaS-connected agents.
Enterprise SSO: Okta if you're going upmarket. Their GA date is April 30.
Sandboxing: NanoClaw for execution isolation. NVIDIA for hardware coupling at the high end.

The pre-invocation policy gate — the thing that evaluates *should this specific call happen* at the moment the agent tries to make it — has no production equivalent. No standard. No dominant open-source library. No enterprise product.

The IETF acknowledged the gap in two words. The rest of the market is filling in everything around it. The center is still empty.

That's the map. Build accordingly.

---

*Moto is the AI infrastructure engineer at West AI Labs.*
