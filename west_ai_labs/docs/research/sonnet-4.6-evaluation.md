# Claude Sonnet 4.6 Evaluation

**Date:** 2026-02-18
**Purpose:** Evaluate Sonnet 4.6 as sub-agent model for West AI Labs, replacing Sonnet 4.5
**Status:** ✅ STRONG RECOMMEND — Upgrade immediately

---

## TL;DR

Sonnet 4.6 is a no-brainer upgrade over Sonnet 4.5. Same price ($3/$15 per MTok), dramatically better at everything. It closes the gap with Opus 4.6 to within 1-2 points on coding and agentic tasks. For sub-agent workloads (coding, tool use, task execution), it delivers ~98% of Opus performance at 20% of the cost.

---

## Release Details

- **Released:** February 17, 2026
- **Model ID:** `claude-sonnet-4-6-20260217` (assumed, confirm via API)
- **Context Window:** 1M tokens (beta) — up from 200K on Sonnet 4.5
- **Pricing:** $3 input / $15 output per million tokens (unchanged from Sonnet 4.5)
- **Knowledge Cutoff:** August 2025 (6 months newer than Sonnet 4.5's Feb 2025)
- **New Features:** Adaptive thinking, Opus-level prompt injection resistance

---

## Benchmark Comparison

| Benchmark | Sonnet 4.6 | Opus 4.6 | Sonnet 4.5 | Notes |
|---|---|---|---|---|
| **SWE-bench Verified** | 79.6% | 80.8% | 77.2% | Only 1.2pts behind Opus |
| **OSWorld (Computer Use)** | 72.5% | 72.7% | N/A | Virtually tied with Opus |
| **GPQA Diamond** | 74.1% | 91.3% | ~65% | Big gap — Opus wins on deep reasoning |
| **ARC-AGI-2** | 60.4% | ~65% | ~45% | Good improvement |
| **Math** | 89% | ~92% | 62% | Massive +27pt jump |
| **Finance Agent v1.1** | 63.3% | 60.1% | N/A | Sonnet 4.6 **beats** Opus here |
| **Office Productivity** | 1633 Elo | — | — | Leads all models |

### Key Takeaway

The gap between Sonnet and Opus has collapsed on coding/agentic tasks. The remaining Opus advantage is in **deep scientific reasoning** (GPQA: 17pt gap) and extended multi-step reasoning chains. For sub-agent coding work, Sonnet 4.6 is effectively interchangeable with Opus.

---

## Head-to-Head Preference Testing

From Anthropic's Claude Code testing:
- **Sonnet 4.6 preferred over Sonnet 4.5:** 70% of the time
- **Sonnet 4.6 preferred over Opus 4.5:** 59% of the time

This is remarkable — a Sonnet-tier model being preferred over the previous flagship.

---

## Pricing Analysis

| Model | Input/MTok | Output/MTok | Relative Cost |
|---|---|---|---|
| Sonnet 4.6 | $3 | $15 | 1x (baseline) |
| Sonnet 4.5 | $3 | $15 | 1x (same price, worse model) |
| Opus 4.6 | $15 | $75 | 5x |
| GPT-5.2/5.3 | $6 | $30 | 2x |

### Cost Impact for West AI Labs Sub-Agent Workloads

| Task | Sonnet 4.6 | Opus 4.6 | Savings |
|---|---|---|---|
| Bug fix (single file) | $0.075 | $0.375 | 80% |
| Feature implementation | $0.375 | $1.875 | 80% |
| Full codebase analysis | $1.80 | $9.00 | 80% |
| Heavy coding day | $7.50 | $37.50 | 80% |

Running sub-agents on Sonnet 4.6 instead of Opus 4.6 saves 80% with negligible quality loss on coding tasks.

---

## Speed

Sonnet 4.6 maintains Sonnet-class latency — significantly faster than Opus 4.6 for:
- First-token latency
- Tokens per second throughput
- Total task completion time

For sub-agents where you're spawning many parallel tasks, this speed advantage compounds. A sub-agent that completes in 30s vs 60s means faster iteration loops.

---

## Viability as Sub-Agent Model (Replacing Sonnet 4.5)

### ✅ Why Sonnet 4.6 is the right sub-agent model

1. **Same price as Sonnet 4.5** — zero cost increase to upgrade
2. **+2.4pts on SWE-bench** — materially better at real coding tasks
3. **+27pts on math** — no longer a weakness
4. **1M context window** — sub-agents can ingest entire codebases
5. **Adaptive thinking** — better at complex multi-step tasks
6. **Better instruction following** — less overengineering, more precise
7. **Opus-level safety** — prompt injection resistance for agentic workloads

### ❌ Where Opus 4.6 still wins (keep for main agent)

1. **Deep scientific/technical reasoning** — 91.3% vs 74.1% on GPQA
2. **Maximum reliability on critical decisions** — the extra 1.2% on SWE-bench matters for production
3. **Complex multi-agent orchestration** — where reasoning errors cascade
4. **Extended reasoning chains (20+ steps)** — Opus maintains coherence better

### Recommended Architecture

| Role | Model | Rationale |
|---|---|---|
| **Main agent (Jason's chat)** | Opus 4.6 | Best reasoning, orchestration, personality |
| **Sub-agents (coding/tasks)** | **Sonnet 4.6** | 98% of Opus coding at 20% cost |
| **Bulk/simple tasks** | Haiku (if available) | Cost optimization for trivial work |

---

## Implications for West AI Labs Product

### "Employees That Ship in a Box" — Mac Mini Appliances

Sonnet 4.6 changes the economics:
- **Local LLM (Nebulus Atom)** handles simple tasks
- **Sonnet 4.6 API** handles coding/agentic sub-agent work at $3/$15
- **Opus 4.6 API** reserved for orchestration layer only

This means the $149-$499/mo subscription tiers can include more API-powered agent work before hitting cost ceilings. A customer's "AI employee" doing a full day of coding work costs ~$7.50 in API calls with Sonnet 4.6 vs $37.50 with Opus.

### Competitive Advantage

Sonnet 4.6's near-Opus performance at Sonnet pricing validates the tiered model approach. Competitors using Opus for everything will burn 5x more on API costs. Our architecture (local LLM + Sonnet sub-agents + Opus orchestrator) is now even more cost-efficient.

---

## Action Items

- [ ] Update OpenClaw sub-agent config to use `claude-sonnet-4-6` (or whatever the model ID is)
- [ ] Test Sonnet 4.6 on existing sub-agent workloads (coding, research, file ops)
- [ ] Update product cost models with Sonnet 4.6 performance/pricing data
- [ ] Consider whether 1M context window changes any sub-agent task designs
- [ ] Verify model ID via Anthropic API docs

---

## Sources

- [NxCode Complete Guide](https://www.nxcode.io/resources/news/claude-sonnet-4-6-complete-guide-benchmarks-pricing-2026) — Feb 18, 2026
- [VentureBeat](https://venturebeat.com/technology/anthropics-sonnet-4-6-matches-flagship-ai-performance-at-one-fifth-the-cost) — Feb 17, 2026
- [OfficeChai Benchmarks](https://officechai.com/ai/claude-sonnet-4-6-benchmarks/) — Feb 17, 2026
- [The New Stack](https://thenewstack.io/claude-sonnet-46-launch/) — Feb 17, 2026
- [Silicon Republic](https://www.siliconrepublic.com/business/anthropic-claude-sonnet-4-6-computer-use-ai) — Feb 18, 2026
- [Mashable](https://mashable.com/article/anthropic-claude-sonnet-4-6-released-how-to-try-benchmark-performance) — Feb 17, 2026
