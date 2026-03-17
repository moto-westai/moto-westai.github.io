# NVIDIA GTC 2026 Keynote Summary

**Date:** March 16, 2026 | **Speaker:** Jensen Huang, CEO & Founder | **Venue:** SAP Center, San Jose, CA

---

## Executive Summary

1. **Inference is the workload of the AI era.** ChatGPT compute has grown 10,000× since 2023. Tokens are the new commodity; compute is revenue. Every company needs an inference strategy.
2. **OpenClaw is "a new operating system for agents."** Jensen named it explicitly on stage. With 300K+ GitHub stars — surpassing React, Linux, and Kubernetes — it is the fastest-growing open-source project in history. NVIDIA built NemoClaw as a reference agent that runs *inside* OpenClaw.
3. **Vera Rubin NVL72 redefines the datacenter.** 50 PFLOPs, 1.6 PB/s HBM4, 10× perf/watt over Blackwell — with day-one commitments from Anthropic, Meta, OpenAI, AWS, Google, Azure, Oracle, CoreWeave, Dell, HPE, Lenovo, and Supermicro.
4. **Groq 3 LPX pairs with Rubin for ultra-high-interactivity inference.** 315 PFLOPs, 128 GB SRAM, 40 PB/s bandwidth — Dynamo routes prefill to Rubin and decode to Groq, yielding 35× efficiency over Hopper at the premium tier.
5. **The revenue-per-gigawatt curve is exponential.** Blackwell ($30B/GW) → Rubin ($150B/GW) → Vera Rubin + LPX ($300B/GW) — a 10× increase in two generations, with 40% of the market in sovereign/enterprise/industrial verticals where West AI Labs operates.

---

## 1. The Inference Inflection

Jensen opened the keynote with a single chart that set the tone for everything that followed: since ChatGPT launched in late 2022, inference compute has grown **10,000×**. This isn't training-driven — it's the compounding demand of hundreds of millions of users generating tokens every second of every day.

He named Claude Code as a 2025 milestone: a coding agent that demonstrated agentic workflows were production-ready. The implication was clear — **tokens are the new commodity**. Every API call, every agent step, every chain-of-thought is inference. And inference is compute. And compute is revenue.

The accompanying slides (`gtc-inference-inflection-10000x.png`, `gtc-inference-inflection-growth-pie.png`) showed inference now dominating NVIDIA's datacenter GPU revenue, with the growth curve still accelerating.

> "Tokens are the new commodity. Compute is revenue." — Jensen Huang

---

## 2. OpenClaw — The Agent Operating System

This was the moment that mattered most to anyone building on OpenClaw. Jensen didn't mention it in passing — he built an entire narrative arc around it.

**"OpenClaw is a new operating system."** Those were his exact words. He positioned it alongside Linux (server OS), Android (mobile OS), and Kubernetes (cloud OS) as the fourth platform shift — the **agent OS**.

The star history chart (`gtc-openclaw-star-history-beats-react-linux.png`, `gtc-openclaw-star-history-full-comparison.png`) was staggering:

| Project | GitHub Stars |
|---------|-------------|
| **OpenClaw** | **300K+** |
| React | 230K |
| Linux | 220K |
| Kubernetes | 115K |
| PyTorch | 95K |

Fastest-growing open-source project in GitHub history. The NVIDIA AI Natives ecosystem slide (`gtc-nvidia-ai-natives.png`) placed OpenClaw alongside Anthropic, OpenAI, Mistral, LangChain, and MCP as the foundational layer of the agentic stack.

And in the closing campfire video (`gtc-openclaw-lobster-cymbals-closing.png`), the OpenClaw lobster mascot was animated playing cymbals among the humanoid robots — a subtle but unmistakable cultural endorsement from Jensen himself.

---

## 3. NemoClaw — NVIDIA's Reference OpenClaw Agent

NemoClaw was announced as NVIDIA's official reference agent for OpenClaw:

```bash
curl -fsSL https://nvidia.com/nemoclaw.sh | bash
```

Critically, **NemoClaw is an OpenClaw plugin, not a separate platform**. It runs inside OpenClaw. The architecture slide (`gtc-nemoclaw-reference-openclaw-architecture.png`) showed the full stack:

- **NeMo** — model training and fine-tuning framework
- **Nemotron** — NVIDIA's flagship open model family
- **Dynamo** — inference routing and orchestration engine
- **cuDF / cuVS** — GPU-accelerated data processing and vector search
- **vGPU** — virtualized GPU sharing for multi-tenant environments
- **AI-Q** — enterprise agent quality and evaluation framework

The announcement slide (`gtc-nemoclaw-for-openclaw-announcement.png`) made the relationship explicit: NVIDIA builds the silicon and the models; OpenClaw is the runtime; NemoClaw is the glue.

**Enterprise implication:** NemoClaw provides capability but not governance. There's no pre-authorization policy enforcement, no DLP, no context isolation between agents. That governance gap is precisely where Conductor fits.

---

## 4. Hardware Announcements

### Vera Rubin NVL72
The headliner. The full-system shot (`gtc-vera-rubin-7chips-5racks-full-system.png`) showed 7 chips across 5 racks — a single logical accelerator delivering:

- **50 PFLOPs** compute
- **1.6 PB/s** HBM4 memory bandwidth
- **10× performance/watt** vs. Blackwell

Launch partners (`gtc-vera-rubin-nvl72-launch-partners.png`): Anthropic, Cursor, Meta, OpenAI, AWS, Google Cloud, Microsoft Azure, Oracle Cloud, CoreWeave, Dell, HPE, Lenovo, Supermicro.

### Vera CPU
A dedicated inference CPU (`gtc-vera-cpu-launch-partners.png`):
- **256 CPU cores**
- **300 TB/s** LPDDR5X bandwidth
- **6.5× throughput** improvement

Launch partners: Meta, Oracle, CoreWeave, Cisco, Dell, HPE.

### GB300 NVL72
Positioned as the current-generation inference king (`gtc-gb300-nvl72-inference-king.png`), bridging to Rubin.

### BlueField-4 STX
Next-gen DPU for network-attached inference (`gtc-bluefield4-stx-launch-partners.png`):
- **5× tokens/sec**
- **50 Tb/s** networking
- **6 TB shared context per GPU**

### Groq 3 LPX
The surprise co-announcement (`gtc-nvidia-groq3-lpx-specs.png`):
- **315 PFLOPs**
- **128 GB SRAM** (no HBM — pure on-chip memory)
- **40 PB/s** internal bandwidth
- **256 chips** per system

Pairs with Rubin via Dynamo routing (`gtc-dynamo-rubin-groq-architecture.png`): Rubin handles prefill (compute-heavy), Groq handles decode FFN (latency-sensitive). Together they deliver ultra-high-interactivity inference.

### NVIDIA Space-1
Rubin GPU module designed for satellites (`gtc-nvidia-space1-vera-rubin-satellite.png`) — orbital inference for Earth observation, communications, and autonomous spacecraft operations.

### Roadmap
The multi-year roadmap (`gtc-nvidia-roadmap-blackwell-rubin-feynman-2028.png`):
- **Blackwell** (2024) — current generation
- **Rubin** (2026) — announced today
- **Feynman / Rosa CPU** (2028) — die stacking architecture

---

## 5. Revenue Opportunity & Economics

Jensen presented the most aggressive revenue-per-gigawatt projections in NVIDIA's history:

| Platform | Revenue per GW | Era |
|----------|---------------|-----|
| Blackwell | $30B | 2024-2025 |
| Rubin | $150B | 2026-2027 |
| Vera Rubin + LPX | $300B | 2027+ |

That's a **10× increase** in two generations (`gtc-rubin-150b-revenue-opportunity.png`, `gtc-rubin-lpx-300b-revenue-10x.png`).

### Pricing Tiers (Inference-as-a-Service)
- **Free tier:** Qwen 3 (open models)
- **$3/query:** Standard
- **$6/query:** Enhanced
- **$45/query:** Premium (long context, complex reasoning)
- **$150/query:** Ultra (400K context window, full agentic)

### Efficiency Curve
The Vera Rubin + LPX combination delivers **35× efficiency vs. Hopper** at ultra-high interactivity workloads (`gtc-rubin-lpx-35x-efficiency-curve.png`), with the Rubin-only path at approximately 10× (`gtc-rubin-inference-performance-efficiency.png`).

---

## 6. Cloud & Partner Ecosystem

Jensen dedicated six full slides to cloud/partner stacks — an unprecedented level of co-marketing:

- **Dell** (`gtc-dell-nvidia-data-platform.png`) — NVIDIA-validated data platform
- **Google Cloud** (`gtc-nvidia-google-stack.png`) — Featured the Snapchat case study: migrated from 45,000 CPUs to 1,000 GPUs with **76% cost savings** (`gtc-google-snapchat-gpu-data.png`)
- **AWS** (`gtc-nvidia-aws-stack.png`) — Humain sovereign cloud, $500B investment
- **Azure** (`gtc-nvidia-azure-stack.png`) — Anthropic partnership
- **Oracle** (`gtc-nvidia-oracle-stack.png`) — OCI infrastructure
- **CoreWeave** (`gtc-nvidia-coreweave-stack.png`) — Serving OpenAI, Mistral, Cursor

### Palantir + Dell Partnership
A notable addition (`gtc-nvidia-palantir-dell-stack.png`): Palantir AIP running on NVIDIA hardware via Dell for enterprise verticals — energy, retail, logistics. This is the "enterprise AI in a box" play.

### DSX AI Factory Platform
NVIDIA's reference architecture for building AI datacenters (`gtc-nvidia-dsx-ai-factory-platform.png`, `gtc-nvidia-dsx-ecosystem-partners.png`): reference designs, Omniverse-based simulation for datacenter layout, and a full construction ecosystem.

### Industry Verticals
Nine verticals with dedicated tracks (`gtc-nvidia-industry-verticals.png`): Automotive, Financial Services, Healthcare, Industrial, Media & Entertainment, Quantum Computing, Retail, Robotics, Telecommunications.

---

## 7. NVIDIA AI Models

### Nemotron 3 Super
The open-model highlight (`gtc-nemotron3-super-best-open-model-openclaw.png`):
- **85.6%** on OpenClaw PinchBench (4th overall, best open model)
- claude-sonnet-4.6 holds #1 at 86.9%
- Positioned as the sovereign AI default — deploy anywhere, no API dependency

### Nemotron 3 Ultra
The flagship (`gtc-nemotron3-ultra-best-open-base-model.png`):
- **5× throughput** vs. GLM on GB200
- **#1** across Understanding, Code, Math, and Multilingual benchmarks

### Nemotron Coalition
NVIDIA announced a coalition of companies building on Nemotron (`gtc-nemotron-coalition-global-ai-leaders.png`):
- Black Forest Labs, Cursor, LangChain, Mistral, Perplexity
- Reflection AI ($2B valuation on $8B raised)
- Sarvam AI (India sovereign AI)
- Thinking Machines (led by Mira Murati, NVIDIA-invested)

### Global Sovereign AI
**16+ countries** building sovereign AI infrastructure on Nemotron (`gtc-world-building-regional-ai-nemotron.png`):
India (×3 initiatives), UAE, Saudi Arabia, Vietnam, Singapore, Indonesia, Korea, Japan, France, Germany/Poland, Spain, EU, Israel.

### Full Model Portfolio
Beyond Nemotron, Jensen showcased the complete model family pipeline (`gtc-nvidia-model-families-pipeline.png`, `gtc-nvidia-model-benchmarks-all.png`):
- **BioNeMo** — drug discovery and molecular simulation
- **Earth-2** — climate and weather prediction
- **Cosmos** — physical world simulation
- **GR00T** — humanoid robotics foundation model
- **Alpamayo** — autonomous vehicles (#1 on LingoQA benchmark at 71.8)

### Open Source Leadership
NVIDIA is now the **world's largest open-source AI contributor by repository count** (`gtc-nvidia-world-largest-osai-contributor.png`):
- Jan–Feb 2025: ~400 repos
- vs. Alibaba (~350), HuggingFace (~280)

---

## 8. Physical AI & Robotics

The stage spectacle (`gtc-physical-ai-robots-caterpillar-stage.png`): a **full-scale CAT 390 excavator**, **15+ humanoid robots**, autonomous vehicles (Mercedes, blue SUV), and a drone — all on stage simultaneously.

Humanoid robot partners represented:
Unitree, Agility Robotics, Boston Dynamics, Figure, 1X, Sanctuary AI, Apptronik, Fourier, Galbot, Agibot, and GR00T-powered prototypes.

**GR00T** serves as the shared AI brain across all physical platforms — a foundation model for embodied intelligence that generalizes across form factors.

Jensen's closing video (`gtc-jensen-campfire-robots-closing-full.png`, `gtc-inference-king-campfire-robots-closing.png`, `gtc-jensen-inference-king-belt.png`) featured the robots gathered around a campfire with Jensen — an homage to the "Inference King" era. The OpenClaw lobster played cymbals.

---

## 9. Enterprise IT Renaissance

Jensen framed the current moment as a fundamental shift (`gtc-enterprise-it-renaissance-saas-to-aaas.png`):

**SaaS → Agent-as-a-Service (AaaS)**

The workforce model changes: humans + AI robots = "Enterprise Information Workers." Every enterprise employee will have AI agents as co-workers, not just tools.

**12 enterprise companies** announced NemoClaw blueprints (`gtc-enterprise-agentic-ai-blueprints.png`):
Adobe, Atlassian, Cadence, Cisco, CrowdStrike, Dassault Systèmes, Palantir, Salesforce, SAP, ServiceNow, Siemens, Synopsys.

NVIDIA positioned the global inference standard (`gtc-nvidia-global-inference-standard.png`) with a market split:
- **60%** — Hyperscaler and AI-native companies
- **40%** — Sovereign, enterprise, and industrial deployments

The agents platform slide (`gtc-agents-new-computing-platform-hd.png`, `gtc-agents-new-computing-platform.png`) made the architectural argument: agents aren't features bolted onto existing software — they're a new computing platform that requires new infrastructure, new operating systems (OpenClaw), and new governance.

---

## 10. West AI Labs Strategic Implications

### We're Already There
West AI Labs runs on the agent OS that Jensen featured as the #1 platform on the world's biggest AI stage. We have a **merged upstream PR (#20076)** in the OpenClaw repository. We are contributors, not consumers.

### Conductor Fills the Gap
NemoClaw provides capability — models, inference routing, GPU acceleration. It does **not** provide governance. No pre-authorization policy enforcement. No DLP. No context isolation between agents. Conductor fills precisely this gap, offering pre-auth policy enforcement vs. runtime filtering.

### Sovereign AI on Nebulus
Nemotron 3 Super at 85.6% PinchBench = a viable local sovereign AI option for the Nebulus Stack. No API dependency, runs on local hardware, deployable in regulated environments.

### The 40% Market
Jensen's own market split says 40% of inference compute goes to sovereign/enterprise/industrial — not hyperscalers. At 1 GW Rubin scale, that's **$120B+ annual opportunity**. West AI Labs plays in this exact segment.

### Employees That Ship in a Box
Jensen's "Enterprise Information Workers" concept maps directly to West AI Labs' "AI Natives" positioning. We're building the agents, the governance layer, and the infrastructure for exactly the workforce transformation Jensen described.

### The Moat
We were building on OpenClaw before Jensen put it on the world's biggest stage. We have upstream commits. We have a governance product (Conductor) that addresses the gap NVIDIA's own reference agent leaves open. We're positioned in the 40% market that the hyperscalers don't serve well.

---

## Key Quotes

> "OpenClaw is a new operating system." — Jensen Huang

> "Tokens are the new commodity. Compute is revenue." — Jensen Huang

> "Inference is the workload." — Jensen Huang

> "AI factories are the industrial infrastructure of the AI era." — Jensen Huang

> "Companies need to have an OpenClaw strategy now." — Post-keynote industry commentary

---

## Images Captured

All screenshots saved to `/memory/gtc-2026/`:

| Filename | Content |
|----------|---------|
| `gtc-inference-inflection-10000x.png` | 10,000× compute growth chart |
| `gtc-inference-inflection-growth-pie.png` | Inference revenue breakdown |
| `gtc-ai-factories-tokens-new-commodity.png` | Tokens = commodity thesis |
| `gtc-openclaw-star-history-beats-react-linux.png` | OpenClaw star history vs. React/Linux |
| `gtc-openclaw-star-history-full-comparison.png` | Full GitHub star comparison |
| `gtc-nvidia-ai-natives.png` | AI Natives ecosystem slide |
| `gtc-agents-new-computing-platform.png` | Agents as new computing platform |
| `gtc-agents-new-computing-platform-hd.png` | HD version of agents platform slide |
| `gtc-nemoclaw-for-openclaw-announcement.png` | NemoClaw announcement |
| `gtc-nemoclaw-reference-openclaw-architecture.png` | NemoClaw architecture diagram |
| `gtc-nemotron3-super-best-open-model-openclaw.png` | Nemotron 3 Super benchmark results |
| `gtc-nemotron3-ultra-best-open-base-model.png` | Nemotron 3 Ultra benchmark results |
| `gtc-nemotron-coalition-global-ai-leaders.png` | Nemotron coalition partners |
| `gtc-nvidia-model-benchmarks-all.png` | Full model benchmark comparison |
| `gtc-nvidia-model-families-pipeline.png` | NVIDIA model family pipeline |
| `gtc-nvidia-world-largest-osai-contributor.png` | NVIDIA OSS contribution stats |
| `gtc-world-building-regional-ai-nemotron.png` | Sovereign AI / 16+ countries |
| `gtc-vera-rubin-7chips-5racks-full-system.png` | Vera Rubin full system |
| `gtc-vera-rubin-nvl72-launch-partners.png` | Rubin NVL72 launch partners |
| `gtc-vera-cpu-launch-partners.png` | Vera CPU launch partners |
| `gtc-gb300-nvl72-inference-king.png` | GB300 NVL72 |
| `gtc-bluefield4-stx-launch-partners.png` | BlueField-4 STX specs |
| `gtc-nvidia-groq3-lpx-specs.png` | Groq 3 LPX specifications |
| `gtc-dynamo-rubin-groq-architecture.png` | Dynamo routing: Rubin + Groq |
| `gtc-rubin-gpu-groq-lpu-specs.png` | Rubin GPU vs. Groq LPU comparison |
| `gtc-nvidia-space1-vera-rubin-satellite.png` | NVIDIA Space-1 satellite module |
| `gtc-nvidia-roadmap-blackwell-rubin-feynman-2028.png` | Multi-year hardware roadmap |
| `gtc-rubin-150b-revenue-opportunity.png` | $150B/GW revenue slide |
| `gtc-rubin-lpx-300b-revenue-10x.png` | $300B/GW with LPX — 10× |
| `gtc-rubin-lpx-35x-efficiency-curve.png` | 35× efficiency vs. Hopper |
| `gtc-rubin-inference-performance-efficiency.png` | Rubin inference perf/efficiency |
| `gtc-dell-nvidia-data-platform.png` | Dell partnership stack |
| `gtc-nvidia-google-stack.png` | Google Cloud partnership |
| `gtc-google-snapchat-gpu-data.png` | Snapchat CPU→GPU migration |
| `gtc-nvidia-aws-stack.png` | AWS partnership (Humain) |
| `gtc-nvidia-azure-stack.png` | Azure partnership (Anthropic) |
| `gtc-nvidia-oracle-stack.png` | Oracle Cloud partnership |
| `gtc-nvidia-coreweave-stack.png` | CoreWeave partnership |
| `gtc-nvidia-palantir-dell-stack.png` | Palantir + Dell enterprise |
| `gtc-nvidia-dsx-ai-factory-platform.png` | DSX AI Factory reference design |
| `gtc-nvidia-dsx-ecosystem-partners.png` | DSX ecosystem partners |
| `gtc-nvidia-industry-verticals.png` | 9 industry verticals |
| `gtc-nvidia-global-inference-standard.png` | Global inference standard / market split |
| `gtc-enterprise-it-renaissance-saas-to-aaas.png` | SaaS → AaaS transformation |
| `gtc-enterprise-agentic-ai-blueprints.png` | 12 enterprise NemoClaw blueprints |
| `gtc-physical-ai-robots-caterpillar-stage.png` | Robots + CAT 390 on stage |
| `gtc-jensen-inference-king-belt.png` | Jensen "Inference King" moment |
| `gtc-jensen-campfire-robots-closing-full.png` | Campfire closing — full shot |
| `gtc-inference-king-campfire-robots-closing.png` | Campfire closing — robots |
| `gtc-openclaw-lobster-cymbals-closing.png` | OpenClaw lobster playing cymbals |

---

*Document prepared for West AI Labs stakeholders. Based on live keynote coverage and slide captures from GTC 2026.*
*Last updated: March 2026*
