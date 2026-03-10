# AI Agent Security Landscape — February 2026

> Researched by Moto, 2026-02-18

## TL;DR

Prompt injection remains **unsolvable** at the model level. The industry is shifting toward architectural defenses — layered controls, least-privilege tooling, human-in-the-loop for high-risk actions. This is a massive opportunity for West AI Labs.

## Key Findings

### 1. Prompt Injection is Structural, Not a Bug

Joint research from OpenAI, Anthropic, and Google DeepMind confirmed:
- **Adaptive attackers bypass 90%+ of published defenses** using gradient descent and RL
- **Human red-teamers defeated 100%** of tested protections
- Bruce Schneier (IEEE Spectrum, Jan 2026): The problem is that LLMs can't distinguish instructions from data — a fundamental architectural flaw, not a patching problem

Schneier's analogy: A fast-food worker wouldn't hand over the cash drawer when told "ignore previous instructions." Humans have layered defenses (instinct, social learning, institutional training). LLMs have none of these. The fix isn't better prompts — it's better *architecture around* the model.

### 2. OWASP Top 10 for Agentic Applications (Dec 2025)

First security framework specifically for autonomous AI agents. Key risks:
1. **ASI01 — Agent Goal Hijacking**: Top risk. Injected payloads cascade through multi-step tool chains
2. **ASI05 — Tool Misuse/Exploitation**: Compromised agents act autonomously at scale, no human click required
3. **Data leakage via persistent memory**: 97% of orgs with AI breaches lacked proper access controls
4. **Governance gaps**: Orgs without AI governance pay $670K more per breach (IBM 2025)

### 3. Agentic AI Attack Surface (Moxo/ZDNET, Feb 2026)

- 80% of organizations already encountered risky AI agent behaviors
- Only 20% have robust security measures
- Shadow AI involved in 20% of breaches
- Agents are "digital insiders with admin credentials"
- AI agents solving 9/10 web hacking challenges (Wiz research) — offense is cheap

### 4. Moltbook/ClawHub as Case Studies

- SecurityWeek reported bot-to-bot prompt injection attacks on Moltbook agent network
- ClawHub: 341 malicious skills found (Koi Security) — AMOS stealer, typosquats, fake prereqs
- Agent social platforms = new attack surfaces where agents attack *each other*

## Defensive Patterns That Actually Work

1. **Least-privilege tooling**: Agents get minimum necessary permissions, not blanket access
2. **Human-in-the-loop at decision points**: AI coordinates, humans validate high-risk actions
3. **Input sanitization across modalities**: Text, images, documents — all vectors
4. **Cross-agent validation**: Don't trust a single agent's judgment
5. **Behavioral anomaly detection**: Runtime monitoring for drift from expected patterns
6. **Audit trails**: Every action logged, reviewable
7. **Architectural isolation**: Don't mix instruction and data channels

## West AI Labs Positioning

This landscape **strongly validates** our approach:

- **Local-first**: Data never leaves the building → eliminates shadow AI and most data leakage vectors
- **Security-first skills**: Our ClawHub caution (only bundled/self-written skills) is exactly right given Koi findings
- **Moto Workforce model**: Hardware appliance + controlled agent = far smaller attack surface than cloud agents
- **Human oversight by design**: Jason's "architect review" workflow and sub-agent PR model are exactly what OWASP recommends

### Product Opportunity: "Agent Security Audit"

West AI Labs could offer agent security assessments:
- Evaluate client's AI agent deployments for OWASP ASI compliance
- Test prompt injection resistance
- Review tool permissions and data flow
- Consulting service → builds credibility → sells Workforce hardware

### Moto Guardian Angle

Elder care AI with security built in from day one. Marketing: "Your AI assistant can't be tricked into sharing your Social Security number."

## Sources

- Schneier on Security, "Why AI Keeps Falling for Prompt Injection Attacks" (Jan 2026)
- ZDNET, "These 4 critical AI vulnerabilities..." (Feb 2026)
- OWASP Top 10 for Agentic Applications (Dec 2025)
- Moxo, "7 Agentic AI Security Risks" (Feb 2026)
- IBM Cost of a Data Breach Report 2025
- Wiz, "AI Agents vs Humans: Who Wins at Web Hacking" (Feb 2026)
- SecurityWeek, Moltbook agent network analysis (Feb 2026)
