# Research Note: aioagent
**Scouted:** 2026-03-03
**Repo:** https://github.com/mariotrerotola/aioagent
**Fork:** https://github.com/moto-westai/aioagent
**Clone:** /home/jlwestsr/projects/research-temp/aioagent
**Stars:** 0 | **Created:** 2026-03-03 | **Last Updated:** 2026-03-03

---

## What It Does

`aioagent` is a brand-new (published today) lightweight multi-agent framework for Python built entirely on `asyncio` with zero external dependencies beyond stdlib. It's a modern alternative to SPADE (which requires an XMPP server), designed for in-process multi-agent simulations, pipelines, and prototypes.

Core concepts:
- `BaseAgent` — subclass + `setup()` to register behaviours
- `MessageBus` — in-process routing via per-agent `asyncio.Queue`
- Behaviours: `OneShotBehaviour`, `CyclicBehaviour`, `PeriodicBehaviour`, `FSMBehaviour`
- FIPA-style messages with performatives (request, agree, refuse, inform), metadata, thread IDs
- `MessageTemplate` — filter behaviours by sender, performative, or metadata
- Broadcast support
- Lifecycle hooks: `on_start()`, `on_end()`
- Published to PyPI as `aioagent`

---

## Architecture Highlights

**Zero infrastructure.** Single-process asyncio event loop. No servers, no brokers, no Docker required. Agents communicate through a shared `MessageBus` backed by `asyncio.Queue` instances.

**FSMBehaviour** enables structured multi-step agent protocols (negotiation, handshakes, multi-stage pipelines) without ad hoc state management.

**FIPA-style messaging** means it has a principled message schema (performative, thread, metadata) which aids routing and filtering — more structured than most ad hoc multi-agent systems.

**Typed and tested:** Ships with mypy type stubs, ruff linting, pytest coverage. Clean, idiomatic Python.

---

## Relevance to West AI Labs / Nebulus Stack

**Moderate-high relevance for Nebulus-Atom.**

The Nebulus-Atom concept is "runtime atoms" — small, composable units of computation. `aioagent`'s behaviour model maps directly: each atom could be an agent with one or more behaviours (cyclic, periodic, FSM-gated). The zero-dependency, single-process, asyncio-native design fits perfectly for lightweight edge deployment on Nebulus-Edge (Apple Silicon).

Specific value:
- **No infrastructure overhead** — ideal for Nebulus-Edge and small-device deployments
- **FSMBehaviour** — could formalize Nebulus-Atom state transitions without custom code
- **FIPA-style threads** — message correlation for multi-step agent interactions (useful for Nebulus-Gantry orchestration)
- **In-process speed** — no serialization overhead for local agent coordination

**Limitations:** In-process only (no distributed/multi-node), no LLM integration built-in, no persistence. Would need to be composed with Nebulus-Core services for memory and inference.

---

## Recommended Next Steps

1. **Spike:** Try wrapping a Nebulus-Atom as a `BaseAgent` with a `CyclicBehaviour` — see if the model fits
2. **FSM for workflows:** Use `FSMBehaviour` to model Nebulus-Gantry workflow steps (propose → validate → execute → report)
3. **Keep an eye on it:** Brand new — author may add distributed/persistence features; watch for v0.2+
4. **Low-risk experiment:** Pure Python, no deps, trivial to add to a Nebulus prototype as a dependency
