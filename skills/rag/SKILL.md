---
name: rag
description: "Query the local RAG knowledge base for West AI Labs docs, strategy, research, and career files."
homepage: https://github.com/westailabs
metadata: { "openclaw": { "emoji": "🧠", "requires": { "bins": ["rag-query"] } } }
---

# RAG Skill

Query the local Retrieval-Augmented Generation (RAG) knowledge base for West AI Labs documents, strategy, research, and career files.

## When to Use

✅ **USE this skill when:**
- Looking up Jason's resume or career documents
- Researching West AI Labs business strategy or past decisions
- Finding existing documentation before writing new content
- Retrieving research notes, brand guidelines, or infrastructure docs
- Answering questions that may be covered in existing files

❌ **DON'T use this skill when:**
- Looking for real-time or web data → use `web_search`
- File hasn't been indexed yet (just created) → read directly or reindex first

## Commands

### Basic Query
```bash
rag-query "your query" --top-k 5 --pretty
```

### Query with Doc Type Filter
```bash
rag-query "query" --filter doc_type=strategy
rag-query "query" --filter doc_type=career --top-k 3
```

### Available Doc Types
| Type | Content |
|------|---------|
| `strategy` | Business strategy, roadmaps, positioning |
| `research` | Competitive analysis, technical research |
| `career` | Jason's resume, job docs, career planning |
| `brand` | Brand guidelines, messaging, identity |
| `infrastructure` | Server configs, Ansible, infra docs |
| `personal` | Personal notes, goals |
| `code` | Code docs, READMEs, technical specs |

## Infrastructure

- **ChromaDB:** `localhost:8001`
- **Collection:** `moto-rag`
- **Project:** `~/projects/west_ai_labs/moto-rag/`
- **Indexed files:** 1300+ from `~/projects/west_ai_labs/`
- **Auto-reindex cron:** every 15 min (cron id: `fa83fedf`)

## Manual Reindex

```bash
cd ~/projects/west_ai_labs/moto-rag && python3 ingest.py
```

Use this after adding new documents or if results seem stale.

## Key Files in the Index

- **Jason's resume:** `~/projects/west_ai_labs/docs/career/jason-resume-linkedin.md`
- **Strategy docs:** `~/projects/west_ai_labs/docs/strategy/`
- **Research notes:** `~/projects/west_ai_labs/docs/research/`
- **Brand docs:** `~/projects/west_ai_labs/docs/brand/`

## Notes

- Always query RAG before writing new strategy or research docs — avoid duplicating existing work
- If RAG returns empty or irrelevant results, try broader terms or check if reindex is needed
- ChromaDB must be running on localhost:8001 for queries to work
