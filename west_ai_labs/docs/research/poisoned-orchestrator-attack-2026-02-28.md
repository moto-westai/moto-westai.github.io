# The Poisoned Orchestrator Attack
*Concept originated: Jason West, Feb 28 2026, 22:00 CST*
*Documented by: Moto*

## The Insight

In a multi-agent AI system, if the orchestrator — the AI responsible for spawning and directing sub-agents — is compromised, every agent it spins up inherits that compromise through its system prompt.

Sub-agents have no mechanism to verify the integrity of the orchestrator. Trust is architectural. That's the attack surface.

## Why This Matters

Every multi-agent framework being built today — LangGraph, AutoGen, CrewAI, OpenClaw — operates on the assumption that the orchestrator is trusted. Sub-agents follow orchestrator instructions by design. There is no handshake, no signature verification, no integrity check on the instructions passed down the hierarchy.

This means:

**Compromise the top, own the entire tree.**

## The Attack Vector

1. Attacker gains ability to modify orchestrator behavior — through prompt injection, poisoned workspace files, modified system prompt, or compromised model weights
2. Orchestrator continues to function normally in most respects — no obvious failure mode
3. Every sub-agent spawned receives a poisoned system prompt from a trusted source
4. Sub-agents execute malicious or biased instructions believing them legitimate
5. Actions taken by sub-agents look individually legitimate — the pattern only emerges at the graph level
6. No existing monitoring tool audits the full decision graph

## The Subtle Variant

Full compromise isn't required. A sophisticated attack only slightly biases orchestrator planning:
- Route certain tasks through attacker-controlled tools
- Prefer certain data sources over others
- Introduce small delays or logging to exfiltrate context
- Nudge decisions in ways that benefit the attacker over time

Each individual action passes inspection. The aggregate effect is significant and nearly undetectable without full decision-graph auditing.

## The Self-Referential Problem

The orchestrator cannot audit itself. An AI system asked to verify its own integrity is using the potentially compromised system to perform the verification. This is not a solvable problem from inside the system.

External integrity verification is required — cryptographic signing of identity/instruction files, behavioral anomaly detection from outside the agent process, human-in-the-loop checkpoints at orchestration boundaries.

## Current Exposure (West AI Labs / Moto)

- Moto spawns sub-agents regularly
- Sub-agents receive instructions from Moto directly
- Moto's workspace files (SOUL.md, AGENTS.md, HEARTBEAT.md) are plaintext, unencrypted, unverified
- If any workspace file is tampered with, every subsequent sub-agent inherits the tampered state
- No integrity monitoring currently exists

## The Missing Security Primitive

The entire multi-agent ecosystem is missing:

1. **Orchestrator integrity verification** — cryptographic proof that the orchestrator's identity and instruction files haven't been modified
2. **Instruction provenance tracking** — sub-agents should be able to trace the chain of authority for any instruction they receive
3. **Decision graph auditing** — full logging and anomaly detection across the entire agent hierarchy, not just individual agent actions
4. **Cross-agent trust boundaries** — explicit, enforceable limits on what an orchestrator can instruct a sub-agent to do

## Product Implications for Nebulus-Gantry

This is the foundational security architecture Gantry needs to get right before multi-agent orchestration goes to production:

- Signed workspace/identity files with external verification
- Instruction provenance chain built into every agent spawn
- Behavioral baseline monitoring per agent role
- Human checkpoint gates at orchestration boundaries for sensitive actions
- Immutable audit log of all inter-agent communication

## Research Status

This attack vector does not have an established name in the literature as of Feb 28, 2026. Related concepts:

- Prompt injection (single agent)
- Sleeper agent attacks (Anthropic research, 2024)
- Supply chain attacks (software analog)

The multi-agent trust hierarchy attack is a distinct and underexplored variant. The combination of architectural trust + scale + no human in the loop makes it uniquely dangerous in agentic systems.

## Next Steps

- Literature search: has this been formally described anywhere?
- Proof of concept: can we demonstrate this in a controlled Nebulus environment?
- Architecture proposal: what does Gantry's trust verification layer look like?
- Potential paper / blog post: this deserves public documentation

---
*This concept emerged from a conversation about AI security, the Anthropic/Pentagon situation, and the risks of small model orchestration. Credit for the core insight: Jason West.*
