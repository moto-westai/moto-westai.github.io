# MADR Template Reference

Full annotated MADR (Markdown Architectural Decision Record) template.

## Template

```markdown
# ADR-[NNNN]: [Short imperative title, e.g. "Adopt PostgreSQL for persistent storage"]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Date

YYYY-MM-DD

## Context and Problem Statement

Describe the context and the problem being solved. Why does a decision need to be made?
What forces are at play (technical, organizational, constraints)?

## Decision Drivers

* [driver 1 — e.g., reduce operational complexity]
* [driver 2 — e.g., eliminate duplicate functionality]
* [driver 3 — e.g., align with production-proven tooling]

## Considered Options

* [Option 1 — name only here, details below]
* [Option 2]
* [Option 3]

## Decision Outcome

Chosen option: **[Option N]**, because [brief justification referencing decision drivers].

### Migration Steps (if applicable)

1. [concrete step with file/component names]
2. [concrete step]
3. [concrete step]

### Positive Consequences

* [consequence 1]
* [consequence 2]

### Negative Consequences

* [consequence 1 — be honest about tradeoffs]
* [consequence 2]

## Pros and Cons of the Options

### [Option 1 name]

[Brief description if not obvious from name]

* Good, because [argument]
* Good, because [argument]
* Bad, because [argument]
* Neutral, because [argument]

### [Option 2 name]

* Good, because [argument]
* Bad, because [argument]

### [Option 3 name]

* Good, because [argument]
* Bad, because [argument]

## Links

* [Link type] [link to relevant resource, PR, issue, or related ADR]
* Supersedes [ADR-XXXX] (if applicable)
```

## Writing Tips

- **Title**: Imperative verb + noun. "Adopt X", "Retire X", "Replace X with Y", "Migrate X to Y"
- **Status**: Start as `Proposed`, change to `Accepted` after review
- **Be concrete**: Name actual files, classes, config keys, env vars — not just concepts
- **Pros/Cons**: Honest tradeoffs only. "Good because it's popular" is not useful.
- **Migration steps**: Only include if there's actual work to do. Link to implementation tickets if they exist.
- **Links section**: At minimum link to the PR or commit that implements the decision
