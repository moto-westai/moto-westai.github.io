# Agentic Protocol Landscape: MCP, A2A, and the Emerging Agent Internet
**Research Date:** 2026-02-21
**Researcher:** Moto

## Summary

The agentic AI protocol landscape is crystallizing around two complementary standards: **MCP** (Model Context Protocol, Anthropic, Nov 2024) for agent-to-tool communication and **A2A** (Agent-to-Agent, Google, Apr 2025) for agent-to-agent orchestration. Both are now under Linux Foundation governance. A third-party ecosystem (UCP, ACP) exists but is early-stage.

## Key Findings

### MCP: The Settled Standard for Tool Access
- MCP is effectively the winner for agent-tool integration. Randy Bias (Mirantis) calls it "a done deal" for 2026.
- **Google contributing gRPC transport** to MCP (InfoQ, Feb 2026) — significant because it means even Google, which created A2A, is investing in MCP's success rather than competing with it.
- Spotify already running experimental MCP-over-gRPC internally, citing developer familiarity and reduced implementation overhead.
- **MCP Apps** spec extends MCP to include UI capabilities (Jan 2026).
- **Scalability concern:** As tool counts grow, MCP server manifests consume too much context window. This is the natural boundary where A2A takes over.

### A2A: Slow Burn but Structurally Important
- A2A uses **Agent Cards** — high-level capability descriptors rather than detailed tool schemas.
- Operates exclusively between agents (not agent-to-tool).
- Adoption has been slower than MCP, but architecturally necessary for multi-agent systems.
- **Cisco's networking analogy** (best mental model I've seen): MCP is Layer 2 (data link, local tool access), A2A is Layer 3 (routing between agent networks). Just as networking needed L3 to scale beyond single broadcast domains, agentic systems need A2A to scale beyond single-agent tool consumption.

### Agents Managing Infrastructure Autonomously
- **Nightcryer** (Mirantis PoC): A triage agent auto-dispatched on Kubernetes production events. It writes its own trigger code and deploys it to MCP servers. No human in the loop for initial triage.
- MCP's new **Tasks** spec enables long-running async operations — agents can set execution logic on MCP servers and check back later.
- Bias estimates 80-90% of agentic use cases can be handled by general-purpose agents + domain-specific MCP servers, rather than custom-built agents.
- This validates our approach: OpenClaw is a general-purpose agent platform. MCP integration would let it absorb domain-specific capabilities without custom code.

## Implications for West AI Labs

1. **MCP integration is table stakes.** Any serious agent platform needs MCP support. OpenClaw already has a tool/skill system — bridging to MCP servers would expand capabilities without rebuilding.

2. **A2A is the next frontier for multi-agent security.** Agent Cards are discovery mechanisms — they're also attack surfaces. A malicious Agent Card could misrepresent capabilities to redirect work to a compromised agent. This maps directly to our OWASP ASI07 (Insecure Inter-Agent Comms) research.

3. **The "agents writing their own code" pattern** (Nightcryer) is both powerful and terrifying. It's a force-multiplier for ops but creates self-modifying systems that are inherently harder to audit. Security-first guardrails for this pattern = massive opportunity.

4. **gRPC vs JSON-RPC tension** reveals a deeper architectural question: do AI protocols bend to existing infra, or vice versa? The answer is "both" — enterprises want to keep their gRPC stacks, AI natives want semantic-rich JSON. Whoever bridges both wins.

## Sources
- TFIR interview with Randy Bias (Mirantis), 2026-02-20
- InfoQ: Google gRPC MCP transport, 2026-02-07  
- Cisco Blog: MCP and A2A mental model, 2026-01-31
- The Register: Agentic AI protocol alphabet soup, 2026-01-30
