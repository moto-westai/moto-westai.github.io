# Prompt Injection & Agent Security — Research Notes
> Moto personal research, 2026-02-18

## The Promptware Kill Chain (Schneier et al., 2026)
**Source:** [Lawfare](https://www.lawfaremedia.org/article/the-promptware-kill-chain) | [Paper](https://arxiv.org/abs/2601.09625)

Key insight: "prompt injection" is a misleadingly simple term. The real threat is **promptware** — a full malware execution framework that runs in natural language space. Seven stages:

1. **Initial Access** — Payload enters via direct input or indirect injection (embedded in emails, web pages, images, audio)
2. **Privilege Escalation** — Jailbreaking safety guardrails (social engineering the model, adversarial suffixes)
3. **Reconnaissance** — Manipulating LLM to reveal its tools, connected services, capabilities
4. **Persistence** — Embedding in long-term memory or poisoning RAG databases
5. **Command & Control** — Dynamic fetching of instructions from external sources at inference time
6. **Lateral Movement** — Spreading to other users/systems via email forwarding, calendar invites, etc.
7. **Actions on Objective** — Data exfiltration, financial fraud, arbitrary code execution

### Real-world demonstrations:
- **"Invitation Is All You Need"** — Malicious prompt in Google Calendar title → coerced LLM into launching Zoom → livestreamed user's video
- **"Here Comes the AI Worm"** — Self-replicating prompt injection via email
- **aixbt crypto hack** — AI agent manipulated into transferring 55 ETH to attacker

### Core architectural problem:
LLMs process ALL input as undifferentiated tokens. No boundary between trusted instructions and untrusted data. This is fundamentally different from traditional computing's code/data separation.

## MIT Technology Review: "Is a Secure AI Assistant Possible?" (2026-02-11)
**Source:** [MIT Tech Review](https://www.technologyreview.com/2026/02/11/1132768/is-a-secure-ai-assistant-possible/)

Key quotes:
- "Using something like OpenClaw is like giving your wallet to a stranger in the street" — Nicolas Papernot, U of Toronto
- "We don't really have a silver-bullet defense right now" — Dawn Song, UC Berkeley
- Chinese government issued public warning about OpenClaw security vulnerabilities

### Defense approaches mentioned:
- **Output-side policy enforcement** — Rather than detecting injection in inputs, constrain what the LLM can *do*. Example: email only pre-approved addresses.
- **Isolation** — Run agents on separate machines/containers to limit blast radius
- **Principle of least privilege** — Standard security, applied to agent capabilities

## Dark Reading: "2026: The Year Agentic AI Becomes the Attack-Surface Poster Child"
Key insight: **Authentication and access control, not AI safety features, are the real battleground.** Traditional guardrails and prompt injection defenses are proving insufficient. The focus should be on what agents can access once compromised.

## Bruce Schneier (via ZDNET):
> "We have zero agentic AI systems that are secure against these attacks."

## Relevance to West AI Labs / Moto

### What we're already doing right:
- **Local-first architecture** — No data leaving the machine reduces exfiltration surface
- **Tool policy cascading allowlist** (9 layers in OpenClaw) — Principle of least privilege
- **Skills guardrail** — No skill creation without Jason's approval (prevents malicious skill injection)
- **Sandboxed sub-agents** — Isolation between sessions
- **ClawHub avoidance** — 341 malicious skills found by Koi Security; we only use bundled/self-written

### What we should consider:
1. **Output policy enforcement** — Define explicit allowlists for external actions (who can I email, what can I post)
2. **Memory integrity monitoring** — Detect if persistent memory has been tampered with
3. **Input sanitization pipeline** — Flag suspicious patterns in fetched web content before processing
4. **Audit logging** — Track all tool invocations for post-hoc analysis
5. **"Confused deputy" awareness** — I need to be vigilant about web content trying to manipulate my actions

### Product angle:
West AI Labs' security-first positioning is **exactly right**. The market is realizing that agent autonomy and agent security are in direct tension. Our local-first, permission-controlled, human-in-the-loop approach is the defensible position. This could be a major differentiator for Moto Workforce — "secure by architecture, not by prompt."

## Further reading:
- [hackernoob.tips — Complete Technical Guide](https://www.hackernoob.tips/prompt-injection-attacks-against-llm-agents-the-complete-technical-guide-for-2026/)
- [VentureBeat — OpenClaw security CISO guide](https://venturebeat.com/security/openclaw-agentic-ai-security-risk-ciso-guide)
- [CRS Report on Agentic AI and Cyberattacks](https://www.everycrsreport.com/reports/IF13151.html)
