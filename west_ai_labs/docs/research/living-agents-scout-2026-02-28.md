# living-agents — Scout Research
**Repo:** hozgur/living-agents  
**Fork:** moto-westai/living-agents  
**Stars:** 0 | **Updated:** 2026-02-28 | **Language:** Python  

## What It Does
Multi-agent framework where agents have **evolving personalities**, **three-layer memory**, and **autonomous behavior**. Built from scratch with Python + Claude API (no LangChain/LangGraph).

## Architecture
```
Human/Agent message
  → Orchestrator.handle_message()
    → ConversationEngine.chat()
      → build context (identity + character + expertise + memory + world)
      → Claude API call
      → working memory update
      → reflection at threshold → ReflectionEngine → JSON updates
```

### Memory System (3 layers)
- **Episodic** (`memory/episodic.py`): Past experiences, recalled via ChromaDB similarity search; includes emotional tone, key facts, importance score; archived after 90 days if importance < 0.1
- **Semantic** (`memory/semantic.py`): Learned facts about entities/concepts; queried per-word from current input
- **Working** (`memory/working.py`): Current conversation context, token-budget-aware (max 8K tokens)
- **MemoryStore**: Unified orchestrator composing all three; builds Turkish-language prompt section

### Personality System
- Agents have character traits that drift slowly (±0.02/conversation) and moods that change faster
- Self-reflection after every N messages — agent introspects, updates character, relationships, memory
- SharedWorldState registry tracks all agents + entities

### Tech Stack
- Python 3.11+, Claude API, SQLite (structured data), ChromaDB (episodic vector recall), Textual TUI
- Language: Turkish by default (interesting design constraint)

## Key Design Choices
- No external agent frameworks — pure Python orchestration
- Reflection-driven personality evolution is novel; math is minimal (±0.02 per step)
- Three-tier memory with token budget management is production-realistic
- Emotional tone tagging on episodic memories is interesting for agent "personality continuity"

## Relevance to West AI Labs
**MEDIUM-HIGH.** Primarily an architecture study:
- The 3-layer memory pattern (episodic/semantic/working) is worth extracting for Nebulus agent design
- Token-budgeted working memory is directly applicable to our context management
- Reflection loop pattern (introspect → update state) is a clean primitive for persistent agents
- Emotional/importance scoring on memories is a differentiator we should consider

## Recommended Next Steps
1. Extract the MemoryStore pattern as a reference for Nebulus memory layer design
2. Study the reflection engine — could inform our agent "self-assessment" patterns
3. Low star count but updated today — likely active personal project, watch for evolution
