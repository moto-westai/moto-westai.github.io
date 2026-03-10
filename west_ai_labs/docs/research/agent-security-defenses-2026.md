# Agentic AI Security: Threats & Defenses (Feb 2026)

> Moto research session — 2026-02-16

## Key Landscape Shifts

The security conversation has moved from "LLM jailbreaking" to **agentic AI security** — agents with persistent memory, tool access, and inter-agent dependencies create fundamentally different attack surfaces than chatbots.

### The Generative → Agentic Shift (StellarCyber)

| Dimension | Generative AI | Agentic AI |
|-----------|--------------|------------|
| Function | Content generation | Action execution |
| Attack vector | Direct prompt injection | Indirect injection + goal hijacking |
| Access level | Read-only sandbox | Read-write API/DB access |
| Memory | Session-based (transient) | Long-term (persistent) |
| Impact | Misinformation | System compromise, financial loss |
| Detection | Pattern-based | Behavioral (deep observability needed) |

Key insight: Traditional SIEM/EDR tools detect human behavioral anomalies. An agent executing an attacker's will 10,000 times looks *normal* to these systems.

## Top Threats (2026)

1. **Prompt injection** — still #1 on OWASP LLM Top 10 (LLM01:2025). Direct and indirect. RAG and fine-tuning do NOT mitigate it.
2. **Tool misuse & privilege escalation** — agents with real tool access can be hijacked to execute arbitrary commands
3. **Memory poisoning** — persistent memory = persistent attack surface. Poison the memory, own future sessions.
4. **Cascading failures** — multi-agent systems amplify single compromises across the chain
5. **NHI (Non-Human Identity) compromise** — hardcoded API keys, leaked credentials (fastest-growing enterprise vector per Huntress 2025)
6. **Supply chain attacks** — compromised skills/plugins/tools
7. **Cross-modal injection** — multimodal models: hide instructions in images that accompany benign text

## Notable Incidents

- **EchoLeak (CVE-2025-32711)**: Infected emails triggered Microsoft Copilot to exfiltrate data *without user interaction* via engineered prompts
- **Moltbook Supabase breach**: 1.5M API keys exposed from vibe-coded backend (our earlier research)

## Defense Frameworks

### OWASP Recommendations
- Constrain LLM access with least privilege
- Human-in-the-loop for privileged operations
- Segregate external content from user prompts
- Establish trust boundaries between LLM, external sources, and tools

### PALADIN Strategy (MDPI paper, Jan 2026)
- Defense-in-depth: no single layer reliably prevents all attacks (LLMs are stochastic)
- Layers: pre-inference input control + post-generation refinement
- Continuous red-teaming + runtime monitoring + privilege minimization

### PromptGuard Framework (Nature, Jan 2026)
- Structured defense coupling pre-inference control with post-generation refinement
- Achieves stronger semantic alignment across heterogeneous LLMs

### Zero Trust for Agents
- Apply Zero Trust not just to humans but to non-human entities
- Every tool call = verify intent, scope, and authority
- Architecture of resilience + verification > fortress mentality

## Federal Activity

- **NIST RFI (Jan 2026)**: Federal Register request for information on AI agent security considerations. Government recognizing agent security as critical infrastructure concern.

## Relevance to West AI Labs

### Our Advantages (Local-First = Security-First)
1. **No cloud exfiltration path** — data stays on-premises by architecture
2. **Tool policy cascading** — OpenClaw's 9-layer allowlist is exactly the right pattern (least privilege per agent)
3. **Memory isolation** — workspace files per agent, not shared cloud memory
4. **Human-in-the-loop built in** — OpenClaw's elevated permissions model
5. **Supply chain control** — skills are local, auditable, version-controlled

### Product Security Positioning
- "Your agent's memory never leaves your network"
- "Zero Trust agent architecture — every tool call verified"
- Memory poisoning is a *cloud* problem when you control the storage
- Our workspace-file memory model (SOUL.md, MEMORY.md) is more auditable than opaque vector DBs

### Gaps to Address
- We need runtime monitoring/observability for agent behavior
- Cross-agent cascading failure protection in multi-agent Nebulus setups
- Formal red-teaming methodology for our own agents
- Input sanitization layer between external content and agent prompts (OpenClaw already does some of this with EXTERNAL_UNTRUSTED_CONTENT wrappers)

## Sources
- OWASP LLM Top 10 (2025): https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- OWASP Agentic AI Top 10 (Dec 2025): https://genai.owasp.org/2025/12/09/
- StellarCyber Agentic AI Threats (2026): https://stellarcyber.ai/learn/agentic-ai-securiry-threats/
- PALADIN defense strategy: https://www.mdpi.com/2078-2489/17/1/54
- PromptGuard framework: https://www.nature.com/articles/s41598-025-31086-y
- Agentic AI Security survey: https://arxiv.org/html/2510.23883v1
- NIST Federal Register RFI: https://www.federalregister.gov/documents/2026/01/08/2026-00206/
