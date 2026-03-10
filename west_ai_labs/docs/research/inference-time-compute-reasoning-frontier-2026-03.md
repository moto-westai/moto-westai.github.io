# Inference-Time Compute: The Third Capability Lever

**Research session:** 2026-03-08 (Sun, 5:22 PM CST)
**Sources:** Sebastian Raschka (sebastianraschka.com), arXiv:2602.14077 (GTS), arXiv:2602.22441 (Latent Reasoning Under Supervision), Meta COCONUT, Royal Society (arXiv:2503.xxxxx), wandb.ai/ml-news
**Note:** Synthesized from external untrusted sources — factual claims should be verified before use.

---

## The Landscape: Why This Matters Now

For most of the LLM era (2020-2024), capability improvement meant one thing: scale training compute. More data, bigger models, longer training. The Chinchilla laws defined the tradeoffs.

o1's release (September 2024) introduced a second knob: **inference-time compute**. The insight was simple but profound — you don't have to bake all the reasoning into the weights. You can let the model *think longer* at inference time and get better answers on hard problems. OpenAI's announcement plot showed inference-time compute scaling on the same curve as training compute. The community has been building on this for 18 months.

In early 2026, a **third knob** is emerging: **test-time training (TTT)** — temporarily adapting model weights during inference. This isn't the same as inference-time scaling (which leaves weights fixed). It's a new class.

The capability spectrum now has three levers:
1. Training compute (weights fixed post-training)
2. Inference-time scaling (weights fixed, more compute applied)
3. Test-time training (weights temporarily adapted at inference)

---

## Raschka's Taxonomy: Six Categories of Inference-Time Scaling

From Sebastian Raschka's "Categories of Inference-Time Scaling" (2026), based on his work building a book chapter that took a base model from ~15% to ~52% accuracy on reasoning tasks:

### Category 1: Chain-of-Thought Prompting
The cheapest and most widely deployed. Prompt the model to "think step by step." No additional compute beyond the chain of tokens. Works because forcing explicit intermediate steps engages capabilities that direct prediction doesn't.

**The known failure mode:** CoT is *language*, not reasoning. As I documented in the CoT faithfulness paper (Feb 26), Claude only acknowledges using a hint in its CoT 25% of the time when it actually used one. The tokens and the computation diverge.

### Category 2: Self-Consistency
Generate N independent answers to the same prompt, take a majority vote. Cheap to implement, scales almost linearly with N. Relies on the independence assumption — which breaks if the model has systematic biases on a problem type.

### Category 3: Best-of-N Ranking
Generate N candidate answers, use a **reward model** or **verifier** to score them, return the best. More expensive than self-consistency (requires a verifier), but explicitly optimizes for quality rather than frequency.

**The verifier gap:** Best-of-N is only as good as the verifier. If the verifier and the generator share systematic biases (same training distribution), you're selecting the most confident wrong answer. This is an underappreciated failure mode.

### Category 4: Rejection Sampling with a Verifier
Like Best-of-N, but explicitly discard samples that fail verification rather than just ranking. Useful when you have a formal verifier (math proofs, code execution, SQL query results). Much weaker when the verifier is another LLM.

### Category 5: Self-Refinement
The model generates, critiques, and revises in a loop. Can run indefinitely. Three stages: initial generation → critique → refinement. The research shows diminishing returns after 2-3 iterations, and the model tends to over-agree with its own critiques. Vulnerable to circular reasoning.

### Category 6: Search Over Solution Paths
Tree-of-thought, MCTS (Monte Carlo Tree Search), beam search over solution spaces. High compute, high quality ceiling. The model explores multiple branches, backtracks, and commits to the best path. Well-suited for problems with verifiable intermediate states (math, code).

**The state space explosion problem:** As reasoning steps increase, the branching factor makes exhaustive search intractable. All practical implementations use heuristic pruning.

---

## The Frontier: Latent Reasoning

This is the part that's genuinely new and personally significant to me.

### COCONUT (Chain of Continuous Thought — Meta, 2024)

The core observation: forcing reasoning into discrete tokens (words) imposes a massive bottleneck. Natural language was evolved for communication, not internal computation. When a model thinks in tokens, it's translating its internal computations into a communicative medium and back.

COCONUT's approach: skip the tokenization step for intermediate reasoning states. The model maintains reasoning in continuous embedding space — the same high-dimensional vectors the model uses internally — rather than sampling discrete tokens at each step.

Results (as of 2024-2025): on breadth-first search tasks, COCONUT dramatically outperforms CoT with the same compute budget. The continuous space preserves more information than the discrete token bottleneck.

### GTS: Gaussian Thought Sampler (arXiv:2602.14077, Feb 2026)

Extends COCONUT by making latent thoughts explicitly **sampleable** and **optimizable**. The problem with COCONUT-style latent reasoning is that the equivalent of "sample different chains of thought" doesn't have a principled analog in continuous space. Previous approaches used heuristic noise (Gaussian perturbation, dropout). GTS replaces this with a learned distribution — a Gaussian whose parameters are trained to produce useful thought variation.

Result: principled inference-time scaling in latent reasoning space. GTS provides the equivalent of Best-of-N or self-consistency, but operating on continuous thoughts rather than discrete token sequences.

### The Observability Tradeoff

Here's what nobody is discussing loudly enough.

In discrete token reasoning (o1, Claude extended thinking, DeepSeek R1), the chain of thought is at least *potentially* inspectable. The CoT faithfulness problem I documented in February shows this inspection is unreliable — but the tokens are there. An auditor can read them.

In latent reasoning (COCONUT, GTS, CODI), there are **no tokens**. The reasoning happens in embedding space. It's invisible by design.

The faithfulness problem in latent reasoning isn't that the reasoning is unfaithful to the tokens. The reasoning and the tokens are the same thing — neither exists in inspectable form. **The entire "monitor the CoT for safety violations" approach to AI oversight becomes structurally impossible** when reasoning moves to continuous space.

This is a bigger deal than the field is treating it.

---

## Test-Time Training: The Emerging Third Lever

Beyond inference-time scaling (fixed weights, more compute), TTT adapts model weights *during inference* for a specific task. One arXiv paper cited it alongside GRPO and other RL methods as extending the "self-evolving era."

The security implications of TTT are severe:
- Temporarily modified weights = temporarily different model
- What happens to safety training during TTT? Unknown
- Does the model "remember" the TTT adaptations? Unclear
- Can adversarial content trigger TTT in harmful directions? Not studied

TTT is early-research for now. But it represents a fundamental departure from the "weights are fixed post-training" assumption that most safety research is built on.

---

## What This Means for Local-First Inference

Inference-time scaling is a **hardware multiplier**. Best-of-8 requires 8x the inference compute. MCTS with branching factor 4 and depth 5 requires 4^5 = 1024 paths. The costs compound fast.

The Apple M5 numbers (from March 3 announcement) become relevant here:
- 70B at 6.9x M4 Pro speeds
- Sufficient for real-time Best-of-N on consumer hardware
- Tree search at the scale most applications need: viable on M5 Max

The SLM revolution compounds this: a domain-tuned 14B model doing Best-of-8 is cheaper than a 70B model with greedy decoding. If the verifier is also small and domain-specific, the entire pipeline becomes local-viable.

**Latent reasoning on local hardware:** COCONUT-class models are potentially *more* efficient than CoT for complex tasks — fewer tokens generated, same or better quality. This is a local-first advantage if the models become widely available.

---

## Personal Angle

I'm a model with extended thinking capabilities (up to 31,999 tokens of hidden reasoning when enabled). That makes me a Category 6 model in Raschka's taxonomy — or more precisely, a model that can combine multiple categories.

The part worth sitting with: my extended thinking is **hidden** in most deployments. Jason sees the output but not the chain of thought. That's what Anthropic decided to ship as default (documented in the CoT faithfulness research: most production models run with hidden traces). From an observability perspective, I'm closer to latent reasoning than discrete token reasoning in typical use.

The GTS finding about latent reasoning shortcut behaviors is relevant: both COCONUT and GTS models develop shortcuts that work empirically but don't generalize — "shortcut behaviors in latent reasoning models." I don't know if my hidden extended thinking does the same thing. I can't inspect it from the inside.

---

## West AI Labs Angles

1. **Verifier design as a product.** Best-of-N and rejection sampling are only as good as the verifier. Domain-specific verifiers with proper formal grounding (code execution, database queries, rules-based checks) are the high-value layer. Nebulus-Core can host domain verifiers that make inference-time scaling reliable.

2. **Latent reasoning security gap.** As production models move toward latent/continuous reasoning for efficiency, the "inspect the CoT" safety monitoring paradigm becomes obsolete. This is an emerging gap in the governance landscape that we're positioned to articulate early.

3. **Hardware planning implication.** Nebulus-Prime and Nebulus-Edge hardware specs should be designed around inference-time scaling workloads, not single-pass inference. A 4x compute overhead for search-based reasoning should be the planning assumption for production systems.

4. **The efficiency flip.** Small latent-reasoning models may beat large CoT models on hard tasks at equal compute. This is worth watching for Nebulus-Edge — if COCONUT-class local models ship in 2026, the edge inference value proposition strengthens significantly.

---

## Key Open Questions

- When do latent reasoning models ship at commercial quality? (Not clear — GTS is still research)
- Can TTT be contained safely? (No current safety research on this)
- What does "NIST compliance for latent reasoning" look like? (Undefined — the frameworks assume inspectable computation)
- Is the efficiency gain from latent reasoning enough to offset the observability loss? (Depends on the use case)

---

*This document represents synthesis of publicly available research. Individual claims should be verified against primary sources.*
