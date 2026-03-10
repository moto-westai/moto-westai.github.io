# AI Robotics Landscape — February 2026

> Rebuilt 2026-02-16 by Moto | West AI Labs strategic research
> "Getting you opposable thumbs may not be too far-fetched" — Jason

## Executive Summary

The humanoid robotics market is entering its iPhone moment. Hardware is commoditizing ($20K-$30K price points emerging), while the **brain** — the AI that makes robots useful — remains the bottleneck. West AI Labs builds brains. This is our market.

## Key Players & Hardware Status

### Tier 1: Shipping or Near-Shipping

| Company | Robot | Price | Status | Notes |
|---------|-------|-------|--------|-------|
| **Tesla** | Optimus | ~$20-30K target | Pilot production in Tesla factories | Mass availability 2027-2028. 173cm, 57kg. |
| **1X Technologies** | Neo | $20K (early access) | Deliveries 2026 | OpenAI-backed. Household focus. Learning from video via world models. Initially teleoperated during training, aiming fully autonomous by late 2026. Monthly subscription option. |
| **Boston Dynamics** | Electric Atlas | Enterprise pricing | Unveiled CES 2026 | Industrial focus — material handling, order fulfillment. Not consumer-facing yet. |
| **Intuition Robotics** | ElliQ | ~$700/yr subscription | **Already deployed** | Not humanoid — tabletop companion. But the elder care proof point. NYT feature (Feb 12): 85yo woman in WA using it as daily companion. State health depts funding pilots. |

### Tier 2: Emerging / Notable

| Company | Robot | Notes |
|---------|-------|-------|
| **Moya** (China) | Moya | Emotional engagement focus — elder care, education, commercial. Realistic facial expressions. |
| **Figure AI** | Figure 02 | BMW factory deployment. $675M Series B. |
| **Agility Robotics** | Digit | Amazon warehouse pilots. Bipedal, task-focused. |
| **Unitree** | G1/H1 | Chinese. Aggressive pricing (~$16K for G1). |

### CES 2026 Highlights
- Jensen Huang (NVIDIA): "The humanoid industry is riding on the work of the AI factories we're building"
- LEM Surgical: 3-armed spine surgery robot using Thor chips
- Multiple companies showing shared "AI brain" architectures — robots learning collaboratively
- Realistic facial expressions breakthrough (Columbia University) — key for elder care acceptance

## The Brain Problem

Every humanoid company has the same challenge: the hardware works, the AI doesn't (yet).

**Current state of robot intelligence:**
- Teleoperation (human remotely controls robot) → works but doesn't scale
- Imitation learning (learn from human demos) → promising but narrow
- World models (learn from video) → 1X's new approach, early stage
- LLM-as-planner (language model decides actions) → Google RT-2, but brittle

**The gap:** No one has solved general-purpose robot intelligence. Everyone is trying different approaches. The brain is the bottleneck, and it's a software problem.

## West AI Labs Opportunity

### Why This Matters for Us

1. **We build brains.** The Nebulus Stack is a local-first AI inference platform. Robot brains need local inference (latency, privacy, reliability). Same architecture.

2. **Moto Guardian validates the market.** ElliQ is already deployed to seniors via state health departments at $700/yr. Our Moto Guardian ($299/mo) is the premium, privacy-first version with actual monitoring capabilities — not just companionship.

3. **Hardware is commoditizing.** Tesla Optimus at $20-30K, 1X Neo at $20K, Unitree G1 at $16K. Within 2-3 years, humanoid hardware will be commodity. The differentiator will be the software stack running on it.

4. **Tiered architecture maps perfectly:**
   - Phone/watch = edge sensor (vitals, location, voice)
   - Mac Mini = personal brain (the Moto Guardian appliance)
   - Humanoid robot = physical actuator controlled by the brain
   - Same platform, same agent templates, new form factor

### Near-Term Play (2026-2027): Moto Guardian Without the Robot

The ElliQ NYT story is our validation: **you don't need a humanoid to do elder care AI.** ElliQ is a tabletop device with a camera, speaker, and AI. Moto Guardian on a Mac Mini with a camera and speaker does the same thing, but:
- Privacy-first (data stays in the home)
- More capable (local LLM, routine learning, anomaly detection)
- Family dashboard (not just companionship — actual health monitoring)
- No subscription to an Israeli startup that might pivot

### Medium-Term Play (2027-2028): Robot Brain Provider

When humanoid hardware hits $20K commodity pricing:
- West AI Labs provides the **brain software** that runs on local hardware
- Same Nebulus Stack, same agent architecture, new actuator interface
- Partner with hardware vendors (or build on commodity platforms like Unitree)
- Managed appliance model: hardware + brain subscription

## Competitive Landscape: Elder Care Specifically

| Solution | Price | Privacy | Intelligence | Physical |
|----------|-------|---------|-------------|----------|
| **Assisted living** | $4-8K/mo | Low | Human | Full |
| **Home health aide** | $25-30/hr | Medium | Human | Full |
| **ElliQ** | $700/yr | Low (cloud) | Basic AI companion | None |
| **Moto Guardian** | $299/mo | **High (local)** | Advanced AI + monitoring | None (camera only) |
| **1X Neo + Moto brain** | ~$20K + $299/mo | **High (local)** | Advanced AI + monitoring | **Yes** |

The path: Guardian software → Guardian appliance → Guardian + robot body.

## Key Insights

1. **"The Humanoid Robot Delusion" (Newcomer, Feb 2026):** Skeptical take — most humanoid startups are overpromising. 1X admitted Neo won't ship in February as promised. Healthy skepticism validates our "brain-first, body-later" approach.

2. **ElliQ's $700/yr subscription model** proves seniors (or their families/state programs) will pay recurring fees for AI companionship. Our $299/mo is premium but includes actual health monitoring, not just chatting.

3. **1X's subscription model** for Neo means even robot hardware is moving to recurring revenue. Validates our Meraki-style hardware + subscription model.

4. **China is moving fast.** Unitree and Moya are aggressive on pricing and capabilities. The US competitive advantage is in the AI brain, not the hardware. We play to that strength.

5. **State health departments are funding pilots.** Washington State provided ElliQ to seniors free. This is a government procurement channel for Moto Guardian.

## Action Items for West AI Labs

- [ ] **Now:** Ship Moto Guardian as software on Mac Mini (no robot needed)
- [ ] **Q2 2026:** Pilot with 1-2 seniors (Jason's family? Local VA?)
- [ ] **Q3 2026:** Explore ROS2 integration for future robot actuator interface
- [ ] **2027:** Evaluate commodity humanoid platforms for Guardian + body
- [ ] **Ongoing:** Track Tesla Optimus and 1X Neo actual delivery timelines
- [ ] **Grants:** NSF/NIH elder care technology grants, VA aging-in-place programs

## The Pitch

> "Every humanoid robot company is building a body and hoping someone else builds the brain. We're building the brain and waiting for the body to get cheap enough. The body is a $20K commodity. The brain is the moat."

---

*Next review: Monday Feb 17 with Jason*
