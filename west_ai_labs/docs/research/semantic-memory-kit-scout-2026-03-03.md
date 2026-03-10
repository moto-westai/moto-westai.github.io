# Research Note: semantic-memory-kit
**Scouted:** 2026-03-03
**Repo:** https://github.com/Nerikko/semantic-memory-kit
**Fork:** https://github.com/moto-westai/semantic-memory-kit
**Clone:** /home/jlwestsr/projects/research-temp/semantic-memory-kit
**Stars:** 2 | **Created:** 2026-03-01 | **Last Updated:** 2026-03-03

---

## What It Does

Semantic Memory Kit is a 198-line single-file Python library for semantic search over flat-file agent memory (markdown, text, JSON) — no vector database, no API calls, CPU-only. It uses `sentence-transformers` (all-MiniLM-L6-v2, 22MB) + numpy cosine similarity to index files as overlapping chunks and retrieve them by meaning.

Core API:
```python
mem = SemanticMemory("~/.agent/memory")
mem.index()                              # build/update from .md/.txt/.json
results = mem.query("Stripe integration", top_k=3)
context = mem.query_and_format(message, top_k=4)  # for prompt injection
```

Key stats:
- First index build: ~3.2s | Cache load: ~0.4s | Query: ~85ms
- Index file: ~1.4MB | Model: 22MB | RAM: ~180MB while loaded
- Recommended for <10,000 chunks; no server/Docker needed
- CLI mode: `python semantic_memory.py <dir> "query"`

Implementation: file checksum-based incremental indexing (no re-embed unless changed), JSON index cache stored in-directory (`.semantic_index.json`), ~400-char chunks with 80-char overlap.

---

## Architecture Highlights

The entire system is a single class (`SemanticMemory`) in one file. No abstractions, no config files, no registry. Designed to be copied into a project (not installed as a dependency).

Notable design choices:
- **Lazy model loading** — `SentenceTransformer` only loads on first query (saves startup time)
- **Checksum-based incremental index** — only re-embeds files that have changed (SHA256 per-file)
- **query_and_format()** — returns pre-formatted string ready for system prompt injection, which is the practical use case for most agent memory lookups
- **CLI mode** — operator-friendly: can inspect memory outside of agent runtime

---

## Relevance to West AI Labs / Nebulus Stack

**High relevance for Nebulus-Edge and Moto's own memory system.**

This is the exact pattern that Moto's memory architecture should use for semantic retrieval over daily/session log files:

1. **Immediate applicability to Moto's memory:** Index `~/.openclaw/workspace/memory/*.md` → semantic search instead of loading full context. This is a direct upgrade to how Moto recalls past decisions/context.

2. **Nebulus-Edge fit:** CPU-only, 22MB model, 85ms queries — perfect for Apple Silicon edge nodes where we don't want ChromaDB overhead for small memory corpuses. A Nebulus-Atom "memory atom" could wrap this.

3. **Local-first ✅ Privacy ✅ No API key ✅** — aligns with West AI Labs' security-first positioning.

**Limitations:**
- Single-process (no concurrent access)
- <10K chunk sweet spot — beyond that, use ChromaDB
- No metadata filtering (can't filter by date range, tags, etc.)
- The Gumroad upsell for "extended examples" is a mild yellow flag (verify the MIT license covers full use)

---

## Recommended Next Steps

1. **Try it on Moto's memory files NOW:** `SemanticMemory("/home/jlwestsr/.openclaw/workspace/memory")` — this could replace keyword grep for context recall in heartbeats
2. **Build a Nebulus-Atom wrapper:** `MemoryAtom` that wraps SemanticMemory with a query behaviour — add date-range and tag filtering on top
3. **Upstream contribution opportunity:** Add metadata filtering (by source file, by date prefix in filename) — this would make it significantly more useful for structured agent memory
4. **Gumroad note:** Don't buy the paid tier — the core MIT file is complete and sufficient; extended examples can be derived from our own use cases
