---
phase: 2
plan: 2
wave: 2
---

# Plan 2.2: Conversational Retrieval Chain (CRC)

## Objective
Implement multi-turn context using LlamaIndex's `CondenseQuestionChatEngine`, solving the core RAG gap of memory awareness.

## Context
- .gsd/SPEC.md
- .gsd/ROADMAP.md
- .gsd/phases/2/RESEARCH.md

## Tasks

<task type="auto">
  <name>Create Chat Engine (CRC)</name>
  <files>src/rag/chat_engine.py</files>
  <action>
    Create a module with a function `build_chat_engine(query_engine)` that returns a `CondenseQuestionChatEngine`.
    - Import `CondenseQuestionChatEngine` and `ChatMemoryBuffer`.
    - Instantiate the engine using:
      `CondenseQuestionChatEngine.from_defaults(query_engine=query_engine, memory=ChatMemoryBuffer.from_defaults(token_limit=1500))`
    - The LLM will automatically use the global `Settings.llm` applied during the QueryEngine setup.
  </action>
  <verify>python -c "from src.rag.chat_engine import build_chat_engine"</verify>
  <done>Chat Engine is successfully instantiated and retains conversational buffer limits.</done>
</task>

## Success Criteria
- [ ] CondenseQuestionChatEngine properly leverages a chat buffer of 1500 tokens to rebuild queries.
