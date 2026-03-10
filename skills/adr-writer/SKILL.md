---
name: adr-writer
description: Draft Architecture Decision Records (ADRs) in MADR format. Use when the user asks to document a technical decision, architectural change, design tradeoff, or deprecation. Triggers on phrases like "write an ADR", "document this decision", "create an ADR for", or "record the decision to".
---

# ADR Writer

Spawn a sub-agent to draft a production-quality ADR in MADR format and save it to the correct location.

## Before Spawning — Gather Context

Collect these before dispatching (ask if not provided):

1. **Decision title** — short, verb-noun form: "Retire X in favor of Y", "Adopt X for Y"
2. **ADR number** — check `[repo]/docs/decisions/` for next sequence number
3. **Target repo path** — where to save the file (e.g., `/home/jlwestsr/projects/west_ai_labs/nebulus-atom/docs/decisions/`)
4. **Context** — what problem existed, what was in place before
5. **The decision** — what was chosen and why
6. **Alternatives considered** — at least 2 options
7. **Consequences** — positive and negative

## Sub-Agent Task Template

```
You are an expert software architect. Draft a production-quality Architecture Decision Record (ADR) in MADR format.

ADR number: [NNNN]
Date: [YYYY-MM-DD]
Title: [verb-noun title]

Context:
[paste gathered context]

The decision:
[paste decision]

Alternatives considered:
[paste alternatives]

Consequences:
[paste consequences]

Requirements:
- Use standard MADR structure (see below)
- Be specific and technical — reference actual file names, component names, config keys
- Include concrete migration steps in the Decision Outcome if applicable
- Be opinionated; this is for engineers who value precision

MADR sections (in order):
# ADR-[NNNN]: [Title]
## Status
## Date
## Context and Problem Statement
## Decision Drivers
## Considered Options
## Decision Outcome
### Positive Consequences
### Negative Consequences
## Pros and Cons of the Options
### [Option 1 name]
### [Option 2 name]
### [Option 3 name if applicable]
## Links

Save to: [full absolute path]/ADR-[NNNN]-[kebab-slug].md
Create the directory if it doesn't exist.
Output a one-line confirmation with the file path when done.
```

## File Naming Convention

`ADR-[NNNN]-[kebab-case-title].md`

Examples:
- `ADR-0012-retire-orchestration-in-favor-of-openclaw.md`
- `ADR-0013-adopt-colima-as-docker-runtime-on-macos.md`

## Status Values

- `Proposed` — drafted, not yet reviewed
- `Accepted` — approved and in effect
- `Deprecated` — superseded by a newer decision
- `Superseded by [ADR-XXXX]` — replaced

## Reference

See `references/madr-template.md` for the full annotated MADR template.
