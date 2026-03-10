# Promptware Kill Chain — Research Notes
*Moto personal research | 2026-02-26*

## Source
Lawfare Media: "The Promptware Kill Chain" (Feb 2026)
arxiv paper: https://arxiv.org/abs/2601.09625

## Core Thesis
"Prompt injection" is too narrow a term. Attacks on LLM-based systems have evolved into a distinct class of **malware execution mechanisms** — the authors call it "promptware." They propose a 7-step kill chain framework mirroring traditional malware campaigns (Stuxnet, NotPetya analogy).

## The Fundamental Vulnerability
LLMs have no architectural boundary between **trusted instructions** and **untrusted data**. Everything — system prompts, user input, retrieved documents, emails — is processed as one undifferentiated token stream. This is structurally different from traditional computing. You can't firewall your way out of it at the model level.

## The 7-Step Kill Chain (partial — article truncated)
1. **Initial Access** — Malicious payload enters the system. Can be direct (typed prompt) or indirect (embedded in retrieved web page, email, shared doc, or even images/audio in multimodal models)
2. **Privilege Escalation** — "Jailbreaking" — bypassing safety training via persona adoption, adversarial suffixes, social engineering the model into ignoring guardrails. Equivalent to escalating to admin in traditional attacks.
3. **Reconnaissance** — Manipulating LLM to reveal system internals, tool schemas, memory contents
4. **(remaining steps not captured — fetch truncated)**

## Defensive Framing from Lawfare
Defense requires **depth at the boundary**, not just prompt-level filtering:
- Limit privilege escalation pathways
- Constrain reconnaissance capability
- Prevent persistence (memory poisoning)
- Disrupt command & control
- Restrict permitted agent actions (least-privilege tooling)

## ZDNet Finding (from search snippet)
Collaborative research from OpenAI, Anthropic, and Google DeepMind found adaptive attackers using **gradient descent and RL bypassed 90%+ of published defenses**. This suggests static rule-based defenses are fundamentally insufficient.

## Microsoft Security Blog Finding
New attack vector: **AI Recommendation Poisoning** — manipulating AI memory stores to corrupt long-term behavior. Defenses: prompt filtering, content/instruction separation, user-visible memory controls.

## MIT Tech Review Angle
Human-in-the-loop agentic workflows are now the attack vector — coercing agents to take harmful real-world actions (calendar writes, email sends, etc.) via injected content.

## Relevance to West AI Labs / Nebulus Stack
- Nebulus-Core's memory layer is a high-value attack target for persistence/poisoning attacks
- Tool permission scoping (least-privilege) is critical and validates the modular Nebulus-Atom approach
- Local-first architecture reduces indirect injection surface vs. cloud-connected agents (no web browsing = fewer retrieval vectors)
- **Moto's own memory files are potential injection targets** — external content written to memory could influence future sessions. Worth noting for OpenClaw's security model.
