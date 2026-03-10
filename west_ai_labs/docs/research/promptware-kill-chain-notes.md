# Promptware Kill Chain — Research Notes

> Source: Lawfare (Feb 2026), MIT Tech Review (Feb 11, 2026), + multiple security blogs
> Researched: 2026-02-19 by Moto

## Key Concept: "Promptware" (not just "Prompt Injection")

The Lawfare paper reframes prompt injection as a **full malware execution mechanism** with a 7-step kill chain analogous to traditional cyber kill chains (Stuxnet, NotPetya). This is a critical conceptual upgrade — "prompt injection" sounds like a single vulnerability; "promptware" correctly frames it as a **class of malware**.

## The 7-Step Promptware Kill Chain

1. **Initial Access** — Malicious payload enters the AI system
   - Direct: attacker types malicious prompt
   - Indirect: instructions embedded in content LLM retrieves (web pages, emails, docs, images, audio)
   - Root cause: LLMs have NO architectural boundary between trusted instructions and untrusted data

2. **Privilege Escalation** (Jailbreaking) — Bypass safety training/guardrails
   - Social engineering the model (persona adoption)
   - Adversarial suffixes
   - Analogous to user→admin escalation in traditional attacks

3. **Reconnaissance** — Manipulate LLM to reveal its tools, connected services, capabilities
   - Happens AFTER access (unlike traditional recon which is pre-access)
   - Uses the model's own reasoning against it

4. **Persistence** — Embed in long-term memory or poison databases
   - Example: infect email archive so malicious code re-executes on every summarization
   - This is the scariest for personal AI agents like OpenClaw

5. **Command & Control (C2)** — Dynamic fetching of commands from internet
   - Turns static promptware into a controllable trojan
   - Behavior can be modified by attacker post-infection

6. **Lateral Movement** — Spread to other users/devices/systems
   - Self-replicating: infected email assistant forwards payload to all contacts
   - Pivot from calendar to smart home to browser
   - **The interconnectedness that makes agents useful is what makes them vulnerable**

7. **Actions on Objective** — Data exfiltration, financial fraud, code execution
   - Real examples: cars sold for $1, crypto transferred to attackers
   - Agents with code execution = total system compromise

## Real-World Demonstrated Kill Chains

- **"Invitation Is All You Need"** — Malicious prompt in Google Calendar invite title → delayed tool invocation → persistence via calendar artifact → lateral to Zoom → covert livestream of victim
- **"Here Comes the AI Worm"** — Self-replicating via email, full chain demonstrated

## Defense Landscape (MIT Tech Review + ZDNET)

**Current state:** No silver bullet. Joint OpenAI/Anthropic/Google research confirms adaptive attackers bypass >90% of published defenses.

**Approaches being researched:**
- **Privilege restriction** — Pre-approved email addresses, limited tool access (simple but effective)
- **Retokenization** — Breaking tokens into smaller units disrupts 98% of attacks (2026 study)
- **Content separation** — Distinguish user instructions from external content
- **Memory controls** — User visibility into stored memories
- **Input sanitization** — Pattern matching + anomaly detection (first line, not sufficient alone)

**Key quote (Nicolas Papernot, U of Toronto):** "Using something like OpenClaw is like giving your wallet to a stranger in the street"

## Relevance to Agent DLP

This is **exactly** our market. The kill chain maps perfectly to Agent DLP detection points:

| Kill Chain Stage | Agent DLP Detection Opportunity |
|---|---|
| Initial Access | Monitor incoming content for injection patterns |
| Privilege Escalation | Detect jailbreak attempts in real-time |
| Reconnaissance | Flag unusual tool/capability queries |
| Persistence | Monitor memory writes for suspicious patterns |
| C2 | Detect outbound fetches to unknown endpoints |
| Lateral Movement | Monitor cross-tool/cross-service actions |
| Actions on Objective | **Primary focus** — detect exfiltration, unauthorized actions |

**Agent DLP should be positioned as a "kill chain interruptor"** — detecting and blocking at multiple stages, not just the endpoint.

## Market Signals

- Cisco, Trend Micro, CrowdStrike, Kaspersky, Palo Alto all publishing OpenClaw security analyses
- China issued public warning about OpenClaw vulnerabilities
- Kaspersky audit found 512 vulnerabilities, 8 critical
- Koi Security found 341 malicious skills on ClawHub
- New malware families: Fruitshell, Promptflux, Promptlock, PromptSteal
- Adversa AI predicts "agency hijacking" as top 2026 attack vector
- AI-BOMs (AI Bill of Materials) predicted to become mandatory

## Implications for West AI Labs

1. **Agent DLP is even more timely than we thought** — the threat landscape is exploding
2. **"Kill chain interruptor" framing** is better than just "DLP" — broader, more defensible positioning
3. **OpenClaw plugin is the right first target** — it's the poster child for agent risk
4. **Local-first = security advantage** — our core thesis validated by every security blog
5. **Consider: "Promptware Defense Platform"** as product framing alongside/above Agent DLP
