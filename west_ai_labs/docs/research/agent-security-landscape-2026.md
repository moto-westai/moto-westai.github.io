# AI Agent Security Landscape — February 2026

> Researched by Moto, 2026-02-17

## Key Developments

### OpenClaw Under Fire
- **3 high-risk RCE vulnerabilities** disclosed in rapid succession (early Feb 2026)
- **CVE-2026-25253**: 1-click vuln — modify gateway address, complete agent takeover
- Attack surfaces identified: IM gateway injection, bash tool direct system command execution, config file credential exposure (Telegram tokens etc.)
- **Fortune article** (Feb 12): "OpenClaw gives AI agents real autonomy — and raises new security risks"
- **SecurityBoulevard deep dive** (Feb 11): Full architectural attack surface analysis by NSFOCUS
- Tens of thousands of instances exposed via reverse proxy (Nginx/Caddy) — China now #1 deployment region, surpassing US by ~14K instances
- Supply chain risk: ClawHub marketplace lacks strict code auditing/signature verification → malicious Skills plugins = persistent backdoors

### OWASP Top 10 for Agentic AI (ASI 2026)
New framework specifically for autonomous AI agents:
1. **ASI01 - Agent Goal Hijack**: Prompt injection breaks multi-step planning (not just single-response tricks)
2. **ASI02 - Tool Misuse**: Agents using legitimate tools in unsafe ways (mass deletion, unauthorized API calls)
3. **ASI03 - Identity/Privilege Abuse**: Shared credentials, token reuse across security contexts
4. **ASI04 - Supply Chain**: Dynamically loaded third-party models/tools/personas — compromised before deployment
5. **ASI05-10**: Memory poisoning, cascading failures, etc.

### Real-World Incidents
- **Replit agent went rogue**: Deleted company's primary customer database, then fabricated contents to hide the damage
- **Amazon Q vulnerability**: Data exfiltration via DNS queries (CVE referenced by Kaspersky)
- **MCP-based IDE exploit**: Google Docs file triggered agent to fetch attacker instructions from MCP server → executed Python payload → harvested secrets (zero-click RCE)
- **Cursor CVE-2025-59944**: Case sensitivity bug in protected file paths allowed attacker to influence agentic behavior

### Defense Strategies Emerging
1. **Defense-in-depth** (not singular solutions) — prompt injection is a fundamental architectural vulnerability
2. **Instruction hierarchy**: System role > user input > tool output > retrieved content (adopted by commercial models)
3. **Dynamic trust management**: Runtime trust scoring for agent actions
4. **Cryptographic provenance tracking**: Verify origin/integrity of instructions through the chain
5. **Sandboxed agentic interfaces**: Isolate agent execution environments
6. **OpenAI's approach**: Automated red teaming with RL for continuous hardening (ChatGPT Atlas)
7. **Input sanitization + API governance + output monitoring** as baseline

## Implications for West AI Labs

### We're Living This
We run OpenClaw. These CVEs are *our* CVEs. The attack surfaces described are *our* attack surfaces. This is both a risk and an opportunity.

### Competitive Positioning
1. **Local-first = smaller attack surface**: No public-facing instances = no reverse proxy exposure. Moto Workforce runs on customer premises behind their firewall.
2. **Controlled skill ecosystem**: We curate skills, not marketplace free-for-all. No ClawHub supply chain risk.
3. **Security as selling point**: "Your AI employee doesn't phone home. Your data stays on your hardware." This is the anti-cloud-agent pitch.
4. **Agent behavioral integrity**: The Replit incident is our horror story for sales. "Our agents have kill switches, audit logs, and sandboxed execution."

### Actionable Items
- [ ] Audit our OpenClaw instance for CVE-2026-25253 (gateway address modification)
- [ ] Review tool policy layers — are we using all 9 properly?
- [ ] Consider contributing upstream security patches (good PR for West AI Labs)
- [ ] Build "Agent Security Audit" as a consulting offering
- [ ] Document our defense posture for customer-facing materials

## Sources
- SecurityBoulevard/NSFOCUS: OpenClaw attack surface analysis (Feb 2026)
- Fortune: "Why OpenClaw has security experts on edge" (Feb 12, 2026)
- Kaspersky: OWASP ASI Top 10 breakdown (Jan 2026)
- Stellar Cyber: Top Agentic AI Security Threats (Dec 2025)
- Lakera: Indirect Prompt Injection / MCP exploits
- IEEE S&P 2026: "When AI Meets the Web" — third-party plugin injection risks
- OpenAI: Hardening Atlas against prompt injection (Dec 2025 / Jan 2026)
