# Kite — Scout Notes (2026-03-02)

**Repo:** https://github.com/thienzz/Kite  
**Fork:** https://github.com/moto-westai/Kite  
**Stars:** 8  
**Language:** Python  
**Clone:** /home/jlwestsr/projects/research-temp/Kite  
**PyPI:** kite-agent

---

## What It Does

Kite is a production-grade Python agentic AI framework built around one core insight: safety logic belongs in code, not in prompts. It treats the LLM as an "untrusted reasoning engine" — the agent proposes actions, the Kite Kernel validates and executes them. This is the "kernel pattern."

---

## Architecture Highlights

- **Kernel Pattern:** Agent proposes → Kernel validates → Kernel executes. No direct LLM-to-action path.
- **Safety modules (kite/safety/):**
  - `guardrails.py` — Pydantic-based structured output enforcement with regex JSON extraction fallback
  - `circuit_breaker.py` — configurable failure threshold, prevents infinite retry loops
  - `kill_switch.py` — hard stop mechanism
  - `idempotency_manager.py` — prevents duplicate side effects
- **4 reasoning patterns** (pipeline/): `reactive_pipeline.py`, `deterministic_pipeline.py`, plus resource router and optimization layer
- **MCP tool servers** included: Slack, Postgres, Google Drive, Gmail, Stripe — all as MCP servers under `kite/tools/mcp/`
- **Monitoring + tracing:** `kite/monitoring.py`, `kite/observers.py`, `kite/caching/` with Redis backend option
- **EventBus:** pub/sub architecture for agent observability. Supports relay URLs for remote event streaming.
- Multi-provider LLM support (`kite/llm_providers.py`), Ollama integration via `tools/diagnose_ollama.py`
- Docker + PyPI packaged. Lightweight (1.8MB clone).

---

## Relevance to West AI Labs

**High.** Kite validates West AI Labs' "safety-first" positioning and provides a concrete reference implementation.

Key alignments:
- "Code over Prompts" safety philosophy = West AI Labs' core security-first positioning. We should be writing blog posts and positioning against frameworks that rely on prompt-based safety.
- Circuit breakers + kill switches + idempotency = the exact patterns Nebulus-Gantry needs for safe multi-agent orchestration.
- Ollama integration + local-first orientation = compatible with Nebulus-Prime/Edge inference stack.
- MCP tool server pattern for Slack/Postgres/etc. = composable with Nebulus-Core.
- EventBus with relay URLs = native telemetry/observability pattern worth studying for Nebulus monitoring.

The guardrail implementation (Pydantic + regex fallback) is worth borrowing directly — it's clean and production-tested.

---

## Recommended Next Steps

1. **Lift the Kernel Pattern** as a named design pattern in West AI Labs documentation. The framing ("LLM as untrusted engine") is exactly how to talk about agent safety.
2. Study `circuit_breaker.py` and `kill_switch.py` — adopt these patterns in Nebulus-Gantry orchestration layer.
3. `pip install kite-agent` and benchmark against LangGraph for a simple Nebulus use case.
4. The safety module structure is clean enough to vendor-copy into Nebulus-Core with attribution.
5. Consider: this aligns well enough that a blog post comparing Kite's kernel pattern to West AI Labs' approach would be good positioning content.
