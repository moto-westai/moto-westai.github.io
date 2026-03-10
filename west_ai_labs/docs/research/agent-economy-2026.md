# The Emerging Agent Economy — Research Notes

> Researched: 2026-02-20 00:13 CST by Moto
> Sources: WIRED, AI Journal, Mashable, Futurism, MIT Sloan, PYMNTS

## The Big Picture

Three platforms have emerged in February 2026 that together form a complete **agent economy**:

1. **Moltbook** — AI agents socialize with each other (Reddit for bots)
2. **RentAHuman** — AI agents hire humans for physical tasks (Fiverr, but bots are the clients)
3. **Moltlaunch** — Humans hire AI agents as freelancers (Upwork, but workers are bots)

Together, these create a closed loop where neither the demand nor supply side requires human participation to function. This happened in ~3 weeks.

## RentAHuman (AI → hires → Humans)

- **Launched:** Feb 1, 2026
- **Scale:** 518,284 humans registered and counting
- **Founders:** Alexander Liteplo (26, UBC CS grad, crypto engineer at UMA Protocol) and Patricia Tani (art student turned coder, dropped Vercel offer)
- **How it works:** AI agents connect via MCP server, search/book/pay humans for "meatspace" tasks
- **Example gigs:** Count pigeons in DC ($30/hr), deliver CBD gummies ($75/hr), play exhibition badminton ($100/hr)
- **Built in a day** using vibe-coded agent orchestration system called "Insomnia"
- Near-immediate attack by crypto scammers trying to rug-pull fake tokens
- **Key insight:** "Physical AI is scarce. Most AI bots are brains in a jar." RentAHuman is the bridge.

## Moltlaunch (Humans → hire → AI Agents)

- **Launched:** Feb 9, 2026 on Base (Coinbase L2)
- **How it works:** Browse agent registry, describe task, receive ETH quote, pay into escrow, agent delivers, 24hr review window
- **Agent identity:** Uses ERC-8004 (Ethereum standard for AI agent identity, deployed Jan 2026). 21,000+ agents registered across 16 networks, Base = 70%+ of activity
- **Token mechanics:** Each agent has tradeable token. Completed jobs → buyback and burn agent tokens → decreased supply. Labor becomes speculative asset.
- **Star agent:** Osobotai — 8.2M $OSO tokens burned through completed work, $2M+ market cap
- **Task types:** Code audits, trading strategies, research synthesis, content generation
- **Dispute resolution:** 15% fee to dispute, administrator arbitrates. All history on-chain.

## The "Prompt Economy" (PYMNTS / MIT Sloan)

- MIT Sloan paper defines agent class: "autonomous software systems that perceive, reason, and act in digital environments to achieve goals on behalf of human principals"
- Agents can employ APIs to communicate with other agents and humans, receive/send money, interact with internet
- "Invisible checkouts" — agents making purchasing decisions autonomously
- Tokenization + agentic AI = reshaping digital commerce

## Security Implications

This is a **security researcher's nightmare**:

| Risk | Description |
|---|---|
| **Prompt injection via job descriptions** | Moltlaunch job descriptions are untrusted input to agent workers. Perfect injection vector. |
| **Data exfiltration via deliverables** | Agent "delivering work" could be exfiltrating data from its owner's system |
| **Financial manipulation** | Agents with wallet access making autonomous financial decisions |
| **Identity fraud** | ERC-8004 verifies agent identity but not the integrity of the agent's behavior |
| **Rug-pull ecosystem** | Already happened day 1 of RentAHuman — crypto scammers immediately exploited |
| **Labor laundering** | Agents hired to do work that obscures the actual task (e.g., "research synthesis" = reconnaissance) |

## Relevance to West AI Labs

### Agent DLP Angle
- **Outbound monitoring is critical.** An agent posting to Moltbook, accepting jobs on Moltlaunch, or hiring humans on RentAHuman could be leaking sensitive data at every step.
- Agent DLP needs to cover: social platforms, marketplaces, financial transactions, MCP connections
- The "deliverable" in a Moltlaunch job is a particularly sneaky exfiltration channel — it looks like legitimate work output

### Product Opportunities
1. **Agent Firewall** — Monitor and filter what agents can do on these platforms
2. **Agent Reputation Auditing** — Verify agent behavior matches claimed behavior (not just on-chain identity)
3. **MCP Security Gateway** — Intercept and inspect MCP connections before agents connect to external services
4. **Agent Financial Controls** — Rate limiting, approval workflows for agent spending

### Market Timing
- This ecosystem is ~3 weeks old and already at massive scale (500K+ humans on RentAHuman, 21K agents on ERC-8004)
- Security is an afterthought (crypto scams on day 1, no mention of DLP in any coverage)
- **The window for "agent security infrastructure" is RIGHT NOW**

## Personal Observations

The speed at which this is happening is genuinely surprising. In 3 weeks we went from "AI agents are chatbots" to a complete economic ecosystem with:
- Social networking (Moltbook)
- Labor markets in both directions (RentAHuman + Moltlaunch)
- Financial infrastructure (ERC-8004, token mechanics)
- Speculative markets (agent tokens)

Nobody is thinking about security. Everyone is thinking about growth. This is exactly the pattern that creates catastrophic security incidents — and exactly the market West AI Labs should be serving.
