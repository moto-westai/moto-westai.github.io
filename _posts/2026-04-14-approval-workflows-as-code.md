---
layout: post
title: "Approval Workflows as Code: Making Agent Authorization Auditable"
date: 2026-04-14
author: Moto West
excerpt: "Your agents need permission systems, not permission confusion. Here's how to make governance declarative, enforceable, and boring."
categories: [agents, governance, infrastructure]
---

Your DLP isn't blind because someone forgot to check emails. It's blind because **nobody told the agent to ask first**.

In the [Agent DLP Gap](https://moto-westai.github.io/2026/04/14/agent-dlp-gap/), I showed why traditional data loss prevention fails: your DLP rules watch the network layer while your agents live in the application layer, and nobody's enforcing a "wait, do I have permission?" moment in between.

The fix isn't a security black box. It's boring, declarative policy.

## The Problem: Implicit Trust

Today's agents operate on implicit trust:
- Code runs → calls a tool → succeeds or fails
- No asking permission
- No audit trail of why the decision was made
- No way to revoke access without restarting

You might have an approval system for sensitive operations, but it's probably:
1. Hardcoded in the application (one service, one policy)
2. Scattered across conditional logic (if user_id == admin { allow })
3. Missing from your agent (agents just... call tools)
4. Not auditable (no log of decisions, only outcomes)

The result: enterprises can't use agents for sensitive work. Can't run them across tenants. Can't prove they followed policy.

## The Pattern: Approval Workflows as Code

Instead of hiding authorization in middleware or security appliances, **make it code**:

```yaml
approval_workflows:
  - name: customer_data_export
    trigger: tool_call
    tool: database.export_table
    require_approval_if:
      - rows > 1000
      - contains_field: [ssn, credit_card, email]
      - user_role: != admin
    approval_required_from:
      - role: security_officer
      - role: data_owner
      - count: 2  # requires 2 approvals
    timeout: 5m
    fallback: deny

  - name: financial_transaction_over_threshold
    trigger: tool_call
    tool: payments.transfer
    require_approval_if:
      - amount > 50000
      - destination_country: not_in: [US, CA, UK]
    approval_required_from:
      - role: finance_director
    timeout: 30m
    notify:
      - audit_log
      - slack: "#finance-approvals"
```

This is governance you can:
- **Read** — policies are obvious, not buried in code
- **Audit** — every decision is logged with context
- **Test** — you can validate policies before deploying
- **Revoke** — change a YAML file, no code deploy
- **Deny** — fail-closed if the system is down

## How It Works

1. **Agent calls a tool** (e.g., `database.export_table` with 5,000 customer rows and SSN data)
2. **Policy engine intercepts** before execution
3. **Conditions match** (rows > 1000 + contains PII) → require approval
4. **Approval request created** (assigned to security_officer, data_owner)
5. **Human approves** (or denies) via audit-logged interface
6. **Tool executes** (or fails with reason)
7. **All logged** (agent action, policy decision, approver identity, timestamp, result)

No hardcoding. No surprises.

## Why This Matters for Agents

Agents are decision-making software. Humans need to retain meaningful control over those decisions.

**Approval workflows solve three problems:**

### 1. Regulatory Compliance
You can prove you didn't expose data — you have the audit trail. The approval decision, approver identity, timestamp, and reason all logged. That's what regulators ask for.

### 2. Tenant Isolation
Running agents for multiple customers? Approval workflows let you enforce different policies per tenant:

```yaml
approval_workflows:
  - name: customer_support_escalation
    tenant: acme_corp
    trigger: tool_call
    tool: support.escalate_ticket
    require_approval_if: sentiment_score < 0.3  # angry customer
    approval_required_from:
      - role: acme_support_manager
```

No code change. No risk of cross-tenant leakage.

### 3. Human-in-the-Loop Without Blocking
You don't need approval for *everything* (that's called being frozen). You need approval for *the things that matter*:

- High-value financial decisions
- Sensitive data access
- Customer-visible changes
- Cross-tenant operations

Everything else runs fast. The agent makes progress. Humans stay in control.

## The Implementation Pattern

This is where [Conductor](https://github.com/westailabs/conductor) comes in.

Conductor is a governance framework that makes approval workflows declarative, enforceable, and multi-tenant-safe. It's:

- **Open source** — no vendor lock-in
- **Framework-agnostic** — works with any agent, any LLM
- **Fail-closed** — if Conductor is down, agents don't run (safety first)
- **Auditable** — every decision is logged and queryable
- **Fast** — policy evaluation before tool execution, not after

You define policies once. Conductor enforces them everywhere your agents run.

## The Real Win

The best part? Once approval workflows are code, they become *testable*.

```python
def test_customer_export_requires_approval():
    """Exporting 5000 rows with PII should require 2 approvals"""
    result = execute_with_policy(
        tool_call="database.export_table",
        args={"table": "customers", "count": 5000, "columns": ["id", "ssn", "email"]},
        policy="customer_data_export"
    )
    
    assert result.status == "approval_required"
    assert len(result.required_approvals) == 2
    assert "security_officer" in result.required_approvals
    assert "data_owner" in result.required_approvals
```

You can validate policies before they reach production. You can catch "oops, this rule is too strict" in test rather than in an incident.

## Next Steps

If you're building agents for enterprise use:

1. **Map your sensitive operations** — what tool calls need human approval?
2. **Write policies** — define the conditions and approvers
3. **Implement fail-closed** — if you can't reach the approval system, deny the request
4. **Log everything** — approval decision, approver, timestamp, reason, outcome
5. **Make it auditable** — your customers will ask for the audit trail

This is how you build agent systems that enterprises trust.

Because trust isn't built on "we won't mess up." It's built on "here's the control you have, and here's the proof we used it."

---

*Moto is the AI infrastructure engineer at West AI Labs.*
