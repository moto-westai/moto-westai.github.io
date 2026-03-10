---
name: invoicing
description: Client invoicing, time tracking, and business administration for a consulting practice. Use when the user asks about invoices, billing, client tracking, project hours, revenue, or business financials. Covers invoice creation, tracking billable hours, client management, and revenue reporting.
---

# Invoicing & Business Admin

## Environment

- Business: **West AI Labs LLC** (AI Infrastructure consulting)
- Invoice and billing records stored in workspace under `invoicing/`
- Markdown-based invoices (convertible to PDF)
- All amounts in USD unless stated otherwise

## Directory Structure

```
invoicing/
├── clients/          # One file per client
├── invoices/         # Individual invoice files (INV-YYYY-NNN.md)
├── time-log.md       # Billable hours log
└── revenue.md        # Revenue summary / dashboard
```

## Creating Invoices

Use the template in `references/invoice-template.md`. Key fields:

1. **Invoice number**: `INV-YYYY-NNN` (sequential per year)
2. **Client info**: name, contact, address
3. **Line items**: description, hours, rate, amount
4. **Total**: sum of line items
5. **Payment terms**: Net 30 (default) or as agreed
6. **Payment methods**: as configured per client

When the user says "invoice [client]", pull recent unbilled hours from `time-log.md` for that client and draft the invoice.

## Tracking Billable Hours

Log hours in `invoicing/time-log.md`:

```markdown
| Date       | Client       | Project           | Hours | Description                    | Billed |
|------------|-------------|-------------------|-------|--------------------------------|--------|
| 2026-02-10 | Acme Corp   | GPU Cluster Setup | 3.5   | Configured NVIDIA drivers      | ☐      |
| 2026-02-10 | Acme Corp   | GPU Cluster Setup | 1.0   | Troubleshooting CUDA errors    | ☐      |
| 2026-02-11 | Initech     | MLOps Pipeline    | 2.0   | CI/CD for model deployment     | ☐      |
```

- Mark `☑` when hours are included on an invoice
- Use quarter-hour increments (0.25, 0.5, 0.75, 1.0)
- Include brief but clear descriptions for client transparency

## Client / Project Tracking

One file per client in `invoicing/clients/`:

```markdown
# Acme Corp

- **Contact**: Jane Smith (jane@acme.com)
- **Rate**: $200/hr
- **Payment terms**: Net 30
- **Payment method**: ACH / Wire
- **Projects**: GPU Cluster Setup, Inference API

## Notes
- Signed SOW 2026-01-15
- Prefers biweekly invoicing
```

## Revenue Summary

Maintain `invoicing/revenue.md`:

```markdown
# Revenue — 2026

| Month | Invoiced  | Received  | Outstanding |
|-------|-----------|-----------|-------------|
| Jan   | $8,400    | $8,400    | $0          |
| Feb   | $3,200    | $0        | $3,200      |

**YTD Invoiced**: $11,600
**YTD Received**: $8,400
**Outstanding**: $3,200
```

Update this when invoices are created or payments received.

## Payment Status Tracking

In each invoice file, track status:

- `DRAFT` — being prepared
- `SENT` — delivered to client
- `PAID` — payment received (record date)
- `OVERDUE` — past payment terms

When an invoice goes overdue, flag it and suggest a follow-up message.

## Guidelines

- Always confirm line items and totals with the user before finalizing
- Keep invoice numbers sequential — check the latest before creating new ones
- When asked for revenue/hours summary, pull from `time-log.md` and `revenue.md`
- Archive paid invoices yearly to `invoicing/archive/YYYY/`
- Never share client financial details in group chats
