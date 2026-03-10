---
name: research
description: Research LLM papers, benchmarks, AI news, competitive landscape, and technical topics. Use when the user asks to find, summarize, or compare AI models, papers, tools, frameworks, or industry trends.
---

# Research

## Tools

- `web_search` — discover papers, articles, benchmarks, news
- `web_fetch` — pull full content from URLs for deeper reading

## Workflow

1. **Clarify scope** — confirm topic, depth, and output format before diving in
2. **Search broadly** — run 2-3 varied queries to triangulate
3. **Fetch & read** — pull the most relevant results with `web_fetch`
4. **Synthesize** — summarize findings in a structured format
5. **Cite everything** — always include source URLs

## Summarizing Papers / Articles

```markdown
## [Paper Title](url)
**Authors:** ...
**Published:** YYYY-MM-DD | **Source:** arXiv / blog / etc.

### Key Contributions
- Bullet the main claims or novel ideas

### Method
- Brief description of approach

### Results
- Key metrics, benchmarks, comparisons

### Relevance
- Why this matters for the user's context
```

## Comparing Models / Benchmarks

Use tables for side-by-side comparison:

```markdown
| Model | Params | MMLU | HumanEval | Cost ($/M tok) | Notes |
|-------|--------|------|-----------|-----------------|-------|
| ...   | ...    | ...  | ...       | ...             | ...   |
```

Always note:
- Benchmark date (scores shift over time)
- Whether results are self-reported or independent
- License / availability

## Tracking Industry News

- Search with `freshness: "pw"` or `"pm"` for recent developments
- Cross-reference multiple sources before reporting claims
- Flag rumors vs confirmed announcements

## Citing Sources

Every claim needs a source. Format:

```markdown
According to [Source Name](url), ...
```

For research summaries, include a **Sources** section at the end:

```markdown
## Sources
1. [Title](url) — brief description
2. [Title](url) — brief description
```

## Key Sources

- **Papers:** arxiv.org, semanticscholar.org, paperswithcode.com
- **Benchmarks:** lmsys.org (Chatbot Arena), paperswithcode.com/sota
- **News:** theverge.com, techcrunch.com, arstechnica.com
- **Models:** huggingface.co, openai.com, anthropic.com, google.deepmind.com

## Output Defaults

- Keep summaries concise unless asked for depth
- Lead with the bottom line, then supporting detail
- Flag uncertainty or conflicting information explicitly
- Save extended research to `references/` as markdown files for future use
