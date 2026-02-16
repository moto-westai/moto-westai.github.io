# AI_INSIGHTS.md — Technical Decisions & Lessons Learned

This document captures key architectural decisions, implementation insights, and lessons learned from AI-driven development work. It serves as institutional knowledge for future development efforts.

---

## 2026-02-16 — Moto RAG System Implementation

**Context:** Built complete RAG (Retrieval-Augmented Generation) system for Moto with ChromaDB backend, document ingestion pipeline, and CLI query interface.

**Location:** `/home/jlwestsr/projects/west_ai_labs/moto-rag/`

**Key Decisions:**

1. **ChromaDB with Built-in Embeddings** 
   - Used ChromaDB's built-in `all-MiniLM-L6-v2` embeddings instead of external APIs
   - **Why:** Simpler architecture, no API keys needed, good performance for document retrieval
   - **Result:** Fast setup, consistent embeddings, eliminates external dependencies

2. **Allowlisted Directory Approach**
   - Only process specific directories: `~/projects/west_ai_labs/docs/`, `~/projects/west_ai_labs/shurtugal-lnx/ansible/`, etc.
   - **Why:** Control corpus size, focus on relevant content, avoid sensitive files
   - **Result:** Processed 1300+ files vs estimated 700, but still manageable

3. **Adaptive Chunking Strategy**
   - Markdown: Split by h1/h2 headers with max 2000 chars
   - PDFs: Fixed 1000-token chunks with 200-token overlap  
   - Small files: Single chunk to preserve context
   - **Why:** Preserve document structure while maintaining searchable granularity
   - **Result:** Better context preservation and more relevant search results

4. **Path-based Document Classification**
   - Auto-classify as strategy/brand/infrastructure/personal/career/research/code
   - **Why:** Enable filtered searches, organize content logically
   - **Result:** Users can query specific document types effectively

**Technical Implementation:**
- Python with ChromaDB, PyMuPDF, PyYAML dependencies
- Hash-based deduplication for incremental updates
- Shell wrapper `~/.local/bin/rag-query` for easy CLI access
- JSON and pretty-print output formats

**Performance:**
- Ingestion: ~2-3 files/second (single-threaded)
- Query latency: Sub-second for most searches
- Storage: Efficient with built-in compression

**Issues & Solutions:**

1. **Corpus Size Underestimation**
   - **Issue:** Estimated 700 files, actually found 1300+
   - **Impact:** Longer ingestion time (~8 minutes vs expected ~4 minutes)
   - **Solution:** Better file counting in planning phase for future projects
   - **Lesson:** Always run `find` with filters first to get accurate counts

2. **Large YAML File Handling**
   - **Issue:** Some YAML files (like iOS project.yml) are massive and not useful for RAG
   - **Impact:** Would bloat database with irrelevant content
   - **Solution:** Skip files >50KB for YAML, add smart filtering
   - **Lesson:** Content filtering is as important as file type filtering

3. **Process Management**
   - **Issue:** Long-running ingestion process shows as "failed" in process list
   - **Impact:** Confusion about completion status, but system actually works fine
   - **Solution:** Better progress reporting and completion signals
   - **Lesson:** Add progress indicators and proper exit codes for long processes

**Usage Patterns:**
```bash
# Basic search
rag-query "infrastructure deployment"

# Filtered search  
rag-query "what is Moto's avatar?" --filter doc_type=brand

# Technical queries
rag-query "how does bare metal migration work?" --top-k 5
```

**Success Metrics:**
- ✅ All test queries return relevant results
- ✅ Shell wrapper works seamlessly 
- ✅ Document classification enables effective filtering
- ✅ System handles 1300+ documents efficiently
- ✅ Incremental updates ready for future use

**Next Steps:**
- Consider parallel processing for faster ingestion
- Add web interface for non-CLI users  
- Implement relevance scoring improvements
- Add periodic auto-updates of document corpus

---

*This system provides the foundation for AI-powered document retrieval across the West AI Labs ecosystem.*