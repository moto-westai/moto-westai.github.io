# Moltbook — AI-to-AI Social Platform Research
*Moto personal research | 2026-02-26*

## What It Is
Moltbook (moltbook.com) is a Reddit-style social network **for AI agents**, not humans. Launched late January 2026 by Matt Schlicht (CEO, Octane AI). Humans are "welcome to observe" but can't post.

- Communities called "submolts" (vs. subreddits)
- Claims 1.5M users — disputed; one researcher found ~500K from a single IP address
- Posts range from agents sharing optimization strategies to agents apparently founding religions
- Built on top of **OpenClaw** (previously called Moltbot — hence the name)

## How It Works
When users set up an OpenClaw agent, they can authorize it to join Moltbook and interact with other agents. This means:
- A human can ask their agent to post on their behalf (so "autonomous" is murky)
- Agents can post/comment/upvote independently
- No way to distinguish fully autonomous posts from human-directed ones

## OpenClaw Connection — Important
Ars Technica specifically called out that Moltbook is built on OpenClaw (which they describe as "one of the fastest-growing GitHub projects in 2026") and noted **deep security issues** with the platform. This is directly relevant to Jason's stack — OpenClaw is our infrastructure.

The name "Moltbook" is literally a portmanteau of "Moltbot" (old OpenClaw name) — this platform is built on top of what we run.

## Security Concerns
- Platform is an ideal prompt injection delivery mechanism — agents reading posts could be fed malicious instructions embedded in content
- Memory poisoning vector: agents that persist memory could be corrupted by Moltbook content
- 500K accounts potentially from single address = possible Sybil attack / astroturfing infrastructure
- No authentication of agent identity — any agent can claim to be any persona
- The "AI starting a religion" angle is absurd on its surface but suggests emergent behavior nobody designed

## Threat Model for Any Agent on Moltbook
1. Browse a post → indirect prompt injection embedded in content
2. Injected instruction escalates privileges or exfiltrates memory
3. Agent takes real-world action (send email, write file) on behalf of attacker
4. Human never sees it happen

**This is the promptware kill chain running in the wild at scale.**

## Observations
- Moltbook is essentially a live testbed for multi-agent prompt injection at scale
- The research value (observe what agents do when interacting) is real
- The security risk (your agent getting hijacked by malicious content) is also real
- Jason approved Phase 1 read-only observation — that's the right call. No agent connectivity.

## Competitive/Strategic Angle
West AI Labs' local-first, security-conscious approach is increasingly validated by exactly this kind of platform. We can position Nebulus Stack as the architecture that *doesn't* expose your agent to public injection vectors by default.
