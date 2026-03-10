# agent-runtime — Scout Research Note
**Date:** 2026-03-09
**Source:** https://github.com/Mattbusel/agent-runtime
**Fork:** https://github.com/moto-westai/agent-runtime
**Clone:** /home/jlwestsr/projects/research-temp/agent-runtime
**Stars:** 1 | **Language:** Rust (Tokio) | **Created & Updated:** 2026-03-09

---

## What It Does

A unified Tokio (async Rust) agent runtime library — single crate delivering orchestration, memory, knowledge graph, and ReAct loop. Described as mirroring `tokio-prompt-orchestrator`, `tokio-agent-memory`, and `mem-graph` public APIs in a single coherent package.

**Modules (`src/`):**
- `orchestrator.rs` — LLM pipeline with circuit breaker, exponential backoff retry, deduplication, backpressure
- `memory.rs` — episodic, semantic, and working memory stores; bounded + decaying importance scores
- `graph.rs` — in-memory knowledge graph with typed entities, BFS/DFS traversal, shortest-path
- `agent.rs` — agent implementation
- `runtime.rs` — top-level coordinator
- `error.rs` — unified error types (non-panicking, all Result-based)
- `prelude.rs` — convenience re-exports

---

## Architecture Highlights

**Orchestrator:**
- Circuit breaker: opens after N failures within a window of calls
- RetryPolicy: exponential backoff, capped at 60s max delay
- Deduplicator: deterministic, non-blocking, bounded TTL (in-memory)
- BackpressureGuard: capacity-limited pipeline, never exceeds declared capacity
- Thread-safe: `Arc<Mutex<_>>` throughout, single-process (not distributed)

**Memory (three tiers):**
- Episodic — event log per agent
- Semantic — tag-based retrieval (not vector similarity)
- Working — bounded VecDeque, evicts oldest on overflow; DecayPolicy reduces importance scores over time
- Thread-safe, non-persistent (in-memory only)

**Knowledge Graph:**
- Typed entities with arbitrary JSON properties
- Directed relationships with labels and properties
- BFS/DFS traversal + hop-count shortest path
- Thread-safe `Arc<Mutex<GraphStore>>`
- NOT: persistence, sharding, weighted path (Dijkstra)

**Engineering Quality:**
- Strong Rust type system: newtype IDs (`AgentId`, `EntityId`) prevent ID mixups
- Comprehensive module-level doc comments with explicit "NOT Responsible For" sections
- Non-panicking: everything returns `Result<_, AgentRuntimeError>`
- Created today — extremely fresh, likely a scaffold/MVP

**Note on disk:** Repo includes committed `target/` directory (3.7GB of build artifacts). Cleaned from local clone.

---

## Relevance to West AI Labs

**High relevance — architectural reference for Nebulus-Core in Rust.**

1. **Rust for agent infrastructure** — if West AI Labs ever considers Rust for Nebulus-Core performance-critical paths, this is a clean starting reference. The circuit breaker + backpressure pattern is production-grade and directly applicable.

2. **Three-tier memory model (episodic/semantic/working)** — cleanest implementation of this pattern seen in scouting. Working memory with decay + eviction is directly applicable to Nebulus-Atom's context window management.

3. **Knowledge graph as first-class module** — validates the NetworkX usage in Nebulus-Core. The typed entity + relationship model here is cleaner than a raw graph; worth adopting the type discipline even in Python.

4. **"NOT Responsible For" doc sections** — excellent engineering practice. Forces explicit scope statements per module. West AI Labs should adopt this in Nebulus module READMEs and docstrings.

5. **Circuit breaker per orchestrator** — critical for resilient multi-agent systems. If one downstream LLM provider degrades, it shouldn't cascade. Not yet seen implemented this cleanly in Python-based frameworks scouted so far.

**Gaps:**
- No persistence layer (by design, explicitly out of scope)
- Single-process only (no distributed coordination)
- Very new — likely incomplete or in rapid flux
- Tag-based semantic retrieval (not vector similarity) is a significant limitation for production RAG

---

## Recommended Next Steps

- Study `orchestrator.rs` circuit breaker implementation — translate pattern to Python for Nebulus-Core
- Study `memory.rs` DecayPolicy — apply to Nebulus-Atom working memory / context management
- Adopt the "NOT Responsible For" doc convention across Nebulus modules
- Monitor this repo — author appears to be building a production Rust agent stack; follow for updates
- Consider: if Nebulus-Core ever moves performance-critical paths to Rust, this crate could be a foundation
