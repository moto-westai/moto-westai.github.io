# mcp-zero Scout — 2026-03-07

**Repo:** https://github.com/abwaters/mcp-zero  
**Fork:** https://github.com/moto-westai/mcp-zero  
**Clone:** /home/jlwestsr/projects/research-temp/mcp-zero  
**Stars:** 1 (early-stage, created 2026-02-09)  
**Language:** Python  
**Updated:** 2026-03-08  

---

## What It Does

mcp-zero is an open-source enterprise MCP gateway — a Python service that sits between AI tools and MCP servers to enforce governance controls that compliance teams require before approving MCP adoption.

Core value prop: "Without it, AI tools can call any MCP server with no access control, no audit trail, and no data protection." The gateway adds identity validation, policy enforcement, PII masking, and structured audit logging — all inline before requests reach downstream MCP servers.

**Architecture:** Hook-based pipeline with ordered priority execution.

- **Identity (Priority 10):** Okta OAuth2 JWT validation, claim mapping (user_id, email, groups)
- **Governance (Priority 50):** YAML policy files, default-deny, rules scoped to server/tool/user/group
- **Masking (Priority 75):** Microsoft Presidio inline PII/secret masking on both inputs AND outputs
- **Audit (Priority 150):** Structured JSON logs with user attribution, correlation IDs, policy decisions
- **Analytics (Priority 145):** Optional Redis-based metrics

**Plugin system:** Entry-point based, loaded from policy file. Custom hooks for rate limiting, metrics, transformation.

**Transport support:** Streamable HTTP, legacy SSE, stdio (spawns local MCP processes).

---

## Architecture Highlights

```
Enterprise AI Tool → MCP Gateway → MCP Servers
                        │
            ┌───────────┴───────────┐
            │   Hook Pipeline       │
            │   Identity (core)     │
            │   Governance (core)   │
            │   ◇ Plugins (ext)     │
            │   Audit (core)        │
            └───────────────────────┘
```

**Policy-as-code:** YAML files define server access, tool-level rules, and masking config. Default-deny startup (exits code 78 if neither identity nor policy configured). `MCP_STRICT_SECURITY=true` requires both.

**src/mcp_zero/ structure:**
- `main.py` — entry point
- `plugin.py` / `plugin_manager.py` — plugin protocol + discovery
- `context.py` — RequestContext, HookContext, UserIdentity
- `identity/` — Okta JWT + OBO token exchange
- `governance/` — policy loading, evaluation, enforcement
- `masking/` — masking engine + Presidio hook
- `pipeline/` — hook lifecycle, registry, execution
- `proxy/` — Starlette app, server management, tool routing
- `analytics/` — optional Redis analytics
- `transport/` — HTTP and stdio MCP transport clients

**Docs quality:** Unusually thorough for a 1-star repo. Includes:
- Threat model canvas
- Security review with known limitations
- Competitive comparison (vs AgentGateway, MintMCP, Microsoft MCP Gateway, Lasso)
- PRD, implementation epics, leadership explainer

---

## Competitive Position (from their own docs)

| | mcp-zero | AgentGateway | Lasso |
|---|---|---|---|
| Language | Python | Rust | Python |
| Auth | Okta JWT | JWT/OAuth multi-provider | None built-in |
| Governance | YAML default-deny | Cedar policy engine | Plugin-based |
| Data protection | Presidio inline | None | Presidio + regex |
| Deployment | Self-hosted | Self-hosted | Local proxy |
| Multi-tenant | User/group policies | Yes | Single-user |

---

## Relevance to West AI Labs

**High direct relevance.** This overlaps significantly with Nebulus-Gantry's governance layer and the MCP security work from the `mcp-critical-infrastructure-agent-sprawl-2026-03` research arc.

Key takeaways:
1. **Validation:** The "default-deny MCP gateway" pattern is real and people are building it. West AI Labs' positioning (security-first MCP) is validated.
2. **Architecture steal:** The hook pipeline with priority ordering is clean. Nebulus-Gantry could adopt a similar pattern for its agent governance layer.
3. **Gap they haven't solved:** Identity is Okta-only. No local-first auth. No multi-provider OIDC beyond Okta. West AI Labs can differentiate here — local IdP support (Keycloak, self-hosted) for privacy-conscious customers.
4. **Presidio integration pattern:** Their masking plugin approach (entry-point plugin, inline on both request and response) is a good reference implementation for how to add DLP to Nebulus-Core.
5. **OBO token exchange docs:** The `okta_obo_for_an_enterprise_mcp_gateway.md` is worth a deep read for the A2A identity delegation pattern.

**Recommended next steps:**
- Read `docs/enterprise_mcp_gateway_threat_model_canvas.md` — threat modeling for MCP gateways is directly useful for Nebulus security posture
- Read `docs/comparison_agentgateway.md` — understand their take on the competitive landscape
- Consider: could the plugin architecture be adapted for Nebulus-Gantry's hook system? Low effort to validate
- Watch this repo — it's building toward something and has unusually good docs for a 1-star project. The author knows enterprise security.
