# mind-swarm — Scout Research Note
**Date:** 2026-03-09
**Source:** https://github.com/ltngt-ai/mind-swarm
**Fork:** https://github.com/moto-westai/mind-swarm
**Clone:** /home/jlwestsr/projects/research-temp/mind-swarm
**Stars:** 2 | **Language:** Python | **Updated:** 2026-03-09

---

## What It Does

Mind-swarm is an experimental "A-Life simulator" where LLM AI drives the cognition of entities called "Cyber." Each Cyber lives inside a Linux chroot filesystem, can navigate/interact with it, and runs a continuous cognition loop with bio-feedback for prioritization. Multiple Cybers share a "swarm" and communicate. Goals are emergent — Cybers are encouraged to explore and learn, provided with "books and lessons."

**Core Concepts:**
- **Cyber** — autonomous LLM agent, each in its own process, rootfs, and cognition loop
- **Bio-feedback** — signals that help prioritize what each Cyber does next (life-forward)
- **Subspace** — shared memory/sync layer between Cybers (configured via `config/subspace_sync.yaml`)
- **ChromaDB** — vector DB for knowledge storage (`chromadb_status.sh`, `config/knowledge_sync.yaml`)
- **Rootfs per Cyber** — `setup_cyber_rootfs.sh`, `manage_cyber_rootfs.sh` — each agent gets a real chroot environment

**Supported LLM Providers (via yaml configs):**
- OpenAI (`config/openai_models.yaml`)
- OpenRouter (`config/openrouter_models.yaml`)
- Cerebras (`config/cerebras_models.yaml`)

**Claude Code sub-agents configured:**
- `.claude/agents/prompt-engineer.md`
- `.claude/agents/ai-engineer.md`
- `.claude/agents/code-reviewer.md`
- `.claude/agents/task-decomposition-expert.md`

---

## Architecture Highlights

- Process-per-agent model — strong isolation, OS-level boundaries
- Chroot filesystem per Cyber — agents have real, isolated environments to live in
- ChromaDB for persistent knowledge, with sync protocols between agents
- Subspace sync for shared state (YAML-configured)
- Bio-feedback loop — non-goal-directed, emergence-driven design
- `.claude/agents/` — project itself uses Claude Code sub-agents for development

---

## Relevance to West AI Labs

**Moderate relevance — mostly as architecture inspiration.**

1. **Process-per-agent with filesystem isolation** — this is the strongest idea here. Chroot per agent is a form of context isolation at the OS level. Nebulus-Atom could adopt something similar: each atom gets a container/namespace, not just a logical boundary. Stronger than TrippleEffect's free-messaging model.

2. **Bio-feedback cognition loop** — interesting for long-running autonomous agents in Nebulus. Rather than task-completion loops, a continuous prioritization signal could make agents more resilient and adaptive.

3. **ChromaDB + subspace sync** — validates West AI Labs' ChromaDB usage for agent memory. The subspace sync protocol between agents is worth examining for Nebulus-Core shared memory design.

4. **Emergence over direction** — philosophically interesting but not suitable for enterprise use cases. West AI Labs' positioning is explicit orchestration with trust, not emergence. Note this contrast when talking to enterprise customers.

**Gaps:**
- Cloud-only LLM providers (no Ollama/local inference)
- Experimental/research quality — not production-grade
- No security/DLP layer; Cyber agents can freely write to their filesystems
- No formal trust or authorization model between agents

---

## Recommended Next Steps

- Read `config/subspace_sync.yaml` and `config/knowledge_sync.yaml` for inter-agent sync patterns
- Study rootfs setup scripts for inspiration on Nebulus-Atom container isolation approach
- The bio-feedback loop concept is worth a separate spike for long-running agent design
- Note: `.claude/agents/` structure is a good pattern to standardize for West AI Labs repos
