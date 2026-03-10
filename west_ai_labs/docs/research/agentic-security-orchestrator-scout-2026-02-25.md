# Research Note: agentic-security-orchestrator
**Scouted:** 2026-02-25  
**Source:** https://github.com/Oiertxo/agentic-security-orchestrator  
**Fork:** https://github.com/moto-westai/agentic-security-orchestrator  
**Clone:** `/home/jlwestsr/projects/research-temp/agentic-security-orchestrator`  
**Stars:** 0 (fresh — 2026-02-25)  
**Language:** Python

---

## What It Does

AI-driven, containerized multi-agent cybersecurity framework using **LangGraph** + **Ollama** (local LLM, Hermes-3). Autonomous agents perform reconnaissance, port scanning, service fingerprinting, and CVE lookups — all inside an isolated Docker network with a hardened Kali Linux engine.

This is a local-LLM-powered penetration testing orchestrator.

---

## Architecture

```
User → Supervisor Agent
         ↓              ↓
    Recon Subgraph   Exploit Subgraph
    ├── ReconPlanner      ├── ExploitPlanner
    └── ReconExecutor     └── ExploitExecutor
         ↓                        ↓
    Kali Engine (FastAPI)    Kali Engine (FastAPI)
    ├── nmap (SYN/version scan)
    ├── NVD Search (CVSS lookups)
    └── Persistent logs
```

### Key Code
- `src/graph.py` — LangGraph `StateGraph` with conditional edges:
  ```python
  supervisor → conditional(next_step) → {recon, exploit, END}
  recon → supervisor  # loop back
  exploit → supervisor
  ```
- `src/state.py` — `AgentState` TypedDict (shared graph state)
- `src/subgraphs/recon/` — ReconPlanner + ReconExecutor subgraph
- `src/subgraphs/exploit/` — ExploitPlanner + ExploitExecutor subgraph  
- `src/agents/supervisor.py` — routes to recon/exploit/finish based on findings
- `services/kali-engine/` — FastAPI server wrapping nmap and NVD API

### LLM
- **Ollama** (local) with **Hermes-3** model
- `src/model.py` — Ollama model initialization
- All reasoning stays local; no cloud LLM calls

### Infrastructure
- Full `docker-compose.yml` — orchestrator + Kali engine + target network
- Isolated Docker network (`10.255.255.0/24`) for safe scanning
- Persistent logs from Kali engine

---

## Relevance to West AI Labs / Nebulus

**Moderate-to-high relevance** — primarily validates our local-LLM-for-security positioning.

1. **LangGraph + local LLMs** — clean example of LangGraph subgraph pattern for task decomposition. Directly applicable to Nebulus-Gantry if we adopt LangGraph as our orchestration primitive.

2. **Local-first security tooling** — West AI Labs is explicitly security-first. This validates that complex security workflows can run entirely on local LLMs. Good client demo fodder.

3. **Supervisor/worker pattern** — the `supervisor → conditional_edge → workers → supervisor` loop is a solid reference for hierarchical agent orchestration in Nebulus-Gantry.

4. **Docker-isolated tool execution** — Kali engine in its own container with a FastAPI interface is an interesting pattern. Could adapt for Nebulus-Atom: dangerous tools (shell exec, network ops) live in sandboxed containers, called via internal API.

5. **Hermes-3 model choice** — noteworthy that they picked Hermes-3 (Nous Research) specifically for agentic/instruction-following tasks. Worth testing in Nebulus inference stack.

### Gaps / Limitations
- Early/WIP state — exploitation subgraph is marked "WIP"
- No auth/access control on Kali engine API (intended for local use)
- Tight coupling to nmap + NVD — limited to network recon use case
- No memory/state persistence across sessions

---

## Recommended Next Steps

1. **Study LangGraph subgraph composition** — `src/subgraphs/recon/recon_subgraph.py` shows how to nest subgraphs. Adopt this pattern for Nebulus-Gantry task routing.

2. **Sandboxed tool execution pattern** — Kali FastAPI wrapper is a clean isolation boundary. Generalize: any "dangerous" tool in Nebulus gets a Docker sidecar with a FastAPI interface.

3. **Hermes-3 benchmark** — add to Nebulus inference test suite (Nebulus-Atom); compare vs. llama-3.1, Qwen2.5, etc. for agentic tasks.

4. **Use as a demo** — a local-LLM security scanner is a compelling West AI Labs client demo: "all your pentest tooling, zero cloud exposure." Build on this concept for a Nebulus showcase.

---

## Notes
- LangGraph conditional edges pattern is clean and minimal — 34 lines total in `graph.py`
- No memory system — each run starts fresh
- The Docker isolation for dangerous tooling is a good safety pattern we should adopt broadly
- Author appears to be Spanish ("Oiertxo") — good international signal of LangGraph adoption
