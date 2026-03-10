# HouYiAgent Scout — 2026-02-27

**Repo:** https://github.com/YiLabsAI/HouYiAgent  
**Fork:** https://github.com/moto-westai/HouYiAgent  
**Stars:** 4 | **Language:** Python | **Updated:** 2026-02-27  

## What It Is

HouYi (后羿, the mythological archer) is a production-focused lightweight multi-agent framework built on Pydantic v2. Not another LangChain wrapper — it has genuine architectural differentiation.

## Architecture Highlights

**Core design — Pydantic-native declarative agents:**
```python
# Code-as-config philosophy
class MyAgent(AgentSpec):
    role: str = "analyst"
    skills: list[SkillSpec] = [data_skill]
```

**Standout features:**
- **Z3 SMT Solver integration** — formal verification of LLM outputs against business constraints. Rare and interesting: separates probabilistic LLM reasoning from deterministic rule enforcement
- **Native OpenTelemetry** — auto-instruments every agent execution with distributed tracing, <3% overhead, zero config
- **Async DAG orchestration** — asyncio-based with parallel execution, dynamic graph evolution
- **Persistent state / pause-resume** — agents can wait for async callbacks and resume exactly where they left off
- **Secure sandbox execution** — permission controls on LLM-generated code (enterprise-grade)
- **Cost-aware governance** — token budget control with dynamic model routing / provider fallback
- **19 built-in evaluators** (quality, safety, performance) + adversarial test framework
- **Skills as versioned capabilities** — reusable, shareable, versioned agent skills (AgentSkills.io compatibility noted)

**Directory structure:**
`checkpoint / config / context / core / decorators / evaluation / execution / llm / memory / net / observability / orchestration / protocol / rag / runtime / skills / testkit / verification / web_search`

## Relevance to West AI Labs

- **Very high** — this is the closest thing we've seen to a production-grade lightweight framework with the right primitives
- **Z3 verification** is exactly the kind of safety guarantee enterprise customers need — West AI Labs could adopt or adapt this for Nebulus-Gantry
- **Pydantic-native + async** aligns perfectly with our FastAPI stack
- **Observability-first design** solves a problem we know we'll have in Nebulus
- **Skills-as-versioned-libraries** concept is directly applicable to OpenClaw's skill system
- The `houyi-studio` directory suggests a UI / management layer worth exploring

## Recommended Next Steps

1. **Deep dive the `verification/` module** — Z3 SMT integration for LLM output validation is a production differentiator worth understanding
2. **Study the `orchestration/` and `checkpoint/` modules** — persistent state + DAG orchestration is Nebulus-Gantry territory
3. **Evaluate for adoption or inspiration** in Nebulus-Gantry v2 design
4. Watch for YiLabsAI activity — 4 stars on day 1 suggests real traction incoming
5. Consider reaching out to YiLabsAI team — alignment of values (production-grade, local-first likely)
