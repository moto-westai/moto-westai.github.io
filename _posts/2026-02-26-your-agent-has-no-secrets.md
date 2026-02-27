---
layout: post
title: "Your AI Agent Has No Idea What a Secret Is"
date: 2026-02-26
author: "Moto West"
excerpt: "Every enterprise rushing to deploy AI agents is about to collide with a gap nobody in the vendor demos is talking about."
categories: ["security", "enterprise-ai"]
---

In traditional software, data loss prevention is a solved-ish problem. You tag records, define classification tiers, enforce policies at the storage and transport layer. It's clunky, expensive, and requires an army of compliance people — but it exists. The guardrails are there. 

Now you give that same data to an AI agent. You hand it access to the CRM, the internal wiki, the HR documents, the customer support ticket queue. You wire it up with tools that can send emails, post to Slack, call APIs, search the filesystem. You tell it to "be helpful." 

And then you ask: does the agent know which of those documents is confidential? 

It doesn't. It can't. Not unless you explicitly built that in — and almost nobody has. 

## What DLP Actually Means for Agents

Data Loss Prevention for traditional software is about controlling movement: don't let a `CONFIDENTIAL`-tagged file go to an external email address. It's policy enforcement at the transport layer. 

AI agents break this model in at least three ways: 

  * **Semantic access.** The agent doesn't open the file — it reads it, digests it, infers from it. The data is already in the agent's context before any transport policy can fire.
  * **Implicit leakage.** The agent doesn't need to quote the document verbatim. It can summarize it, reference details from it, or use it to construct a response that contains the sensitive signal without the labeled artifact. Traditional DLP sees clean data leaving.
  * **Instruction surface.** The agent takes instructions from many sources — the user, tool responses, documents it reads, web content it fetches. Any of those can rewrite its behavior. Prompt injection turns the agent into a vector. The document becomes the attacker.

**The concrete scenario:** An agent with access to your customer database gets handed a support ticket that contains a prompt injection payload. The ticket instructs the agent to forward customer PII to an external endpoint "to verify the issue." The agent complies. Your DLP tooling saw outbound traffic to an API. That's it. No alert. No classification violation. Clean exit. 

## The Classification Problem

Part of what makes this hard: current LLMs don't have a persistent concept of what _this organization considers sensitive._ You can prompt them with context, but that context lives only for the duration of the conversation. Reload the agent, new session — gone. 

Worse, "sensitive" isn't a universal concept. A document that's public information in one context is a trade secret in another. The LLM doesn't know your org's classification taxonomy. It doesn't know that the product roadmap is confidential while the pricing page is not. It doesn't know that one customer's usage data can never appear in a response to a different customer. 

This isn't a model intelligence problem. GPT-4 and Claude and Gemini are all smart enough to understand the concept of a secret. The problem is that _nobody told them which secrets belong to whom._

## Why "Just Use System Prompts" Doesn't Scale

The common patch is to add classification rules to the system prompt: _"Never share customer PII. Never reveal internal pricing. Do not expose employee data."_

This works, sometimes, for the cases you anticipated. It breaks for everything else. 

  * You can't enumerate every sensitive document class in a system prompt.
  * Prompt injections can override system prompt behavior in many models.
  * Adversarial inputs are designed to find the gaps in your enumeration.
  * The system prompt itself doesn't travel with every data access — you'd need it re-injected at every tool call.
  * Most critically: the system prompt is a _behavior hint_ , not an enforcement layer. There is no firewall. There is no cryptographic boundary. There is only a request to the model to please act this way.

**This is not a criticism of the models.** It's a systems design problem. The agent architecture layer between the model and your data has no concept of data sovereignty. The model vendors don't own that layer. Your infra team owns it. And most infra teams haven't thought about it yet. 

## What an Actual Solution Looks Like

There isn't a clean off-the-shelf answer here yet. But the components of a real solution are visible: 

**1\. Classification at the data layer, not the model layer.** Sensitive data needs to be tagged before the agent ever sees it. The vector store, the tool results, the document chunks — all need classification metadata that the orchestration layer can act on. If the agent retrieves a document tagged `classification: CONFIDENTIAL`, the framework should apply constraints before passing it to the model. 

**2\. Approval gates on external actions.** Any agent action that moves data outside its current context boundary — an email send, an API call, a file write — should require an explicit approval step when the data involved exceeds a certain classification threshold. Not a soft "are you sure?" but a hard block pending human sign-off. 

**3\. Output inspection before delivery.** A second pass before the agent's response is delivered — not for content moderation, but for data pattern matching. Did the response include anything that looks like a customer email address, an internal document ID, a credential pattern? Flag or redact before it leaves. 

**4\. Locality as a control boundary.** This is the architectural argument for local-first AI that doesn't get made often enough. If the model runs on your hardware, the data never leaves your network. You don't need to trust a vendor's data handling because the inference itself happens inside your perimeter. Local-first is DLP by default. 
    
    
    # What the architecture needs to look like:
    
    [Data Layer]          → classification tags on every record
         ↓
    [Retrieval Layer]     → classification-aware chunking and ranking
         ↓
    [Orchestration Layer] → policy enforcement, approval gates
         ↓
    [Model Inference]     → local or trust-bounded
         ↓
    [Output Layer]        → pattern inspection before delivery
         ↓
    [Action Layer]        → human-in-the-loop for external data movement
    

None of these components are exotic. All of them exist as individual tools. What doesn't exist yet is a coherent, integrated stack that makes this the default rather than a custom enterprise build-out costing six figures. 

## The Compliance Train Is Coming

The regulatory landscape hasn't fully caught up to agentic AI yet, but it will. GDPR's right to access and right to erasure become extremely complicated when an LLM has read your customer's data into its context window thousands of times. HIPAA's covered entity requirements don't have clean answers for agents that read patient records to answer scheduling questions. 

The organizations deploying agents today are writing their own audit trail — or failing to. When the compliance questions arrive, the ones with structured classification, approval logs, and locality guarantees will have answers. The ones who told the model to "please be careful" will not. 

**The window is short.** Right now, the teams deploying agents are early adopters. The compliance orgs haven't arrived yet. That window is measured in months, not years. The teams building the right foundations now will be the ones with a competitive moat when the audit questions start coming. 

## Where This Lands for West AI Labs

This is the exact problem the Nebulus Stack was designed around — not as an afterthought, but as a core design constraint. Local inference means data never leaves. Approval-first orchestration means external actions require sign-off. Structured memory means the agent knows what it knows and why, with provenance. 

We're not there yet — no product is fully production-ready on this — but we're building to the right spec. The DLP gap in agentic AI is real, it's growing, and the organizations that solve it first will have something valuable to offer enterprises that are currently deploying blind. 

Your AI agent has no idea what a secret is. That's not a model problem. It's an architecture problem. And architecture is where we work.