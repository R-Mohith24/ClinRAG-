---
phase: 2
level: 2
researched_at: 2026-03-09
---

# Phase 2 Research

## Questions Investigated
1. How to integrate a 4-bit quantized GGUF model (BioMistral-7B) into LlamaIndex using CPU-optimized `llama.cpp`?
2. How to implement the Conversational Retrieval Chain (CRC) inside LlamaIndex to rewrite queries dynamically using chat history?

## Findings

### BioMistral LLM Integration via LlamaCPP
LlamaIndex natively supports `llama.cpp` through the `llama_index.llms.llama_cpp.LlamaCPP` class.
**Recommendation:**
- Instantiate `LlamaCPP` pointing to the local GGUF model path.
- Configure context window (`context_window=3900`), max tokens (`max_new_tokens=512`), and temperature (`temperature=0.1` for factual medical responses).
- To run on CPU optimally, do not set GPU layers. 

### Conversational Memory (CRC)
The `CondenseQuestionChatEngine` is designed exactly for this. It takes a `ChatMemoryBuffer` and a standard `QueryEngine`.
**Mechanism:**
1. A user asks a follow-up question ("What are the symptoms?").
2. The engine uses the LLM (BioMistral) to "condense" the chat history + follow-up into a standalone query ("What are the symptoms of Type 2 Diabetes?").
3. This condensed query is sent to the QueryEngine (Retrieval step).
4. The LLM generates the final answer based purely on the retrieved context.

**Recommendation:**
- Extract the LLM setup to its own module (`src/llm/biomistral.py`).
- Create a clear instantiation function for the Chat Engine (`src/rag/chat_engine.py`) that wires the index to the `CondenseQuestionChatEngine` with a `ChatMemoryBuffer`.

## Decisions Made
| Decision | Choice | Rationale |
|----------|--------|-----------|
| LLM Framework | `llama-index-llms-llama-cpp` | Best optimized CPU inference for GGUF formats natively supported by LlamaIndex. |
| CRC Strategy | `CondenseQuestionChatEngine` | Provides exactly the multi-turn context extraction defined in the PRD, clearly separating the 'query rewriting' from 'answer generation'. |

## Patterns to Follow
- Hardcode the expected model path to `models/llm/biomistral-7B-Q4_K_M.gguf`. (The actual download will be handled by the user or an initialization script later).
- Ensure the prompt for condensing the query strictly emphasizes medical accuracy.

## Dependencies Identified
| Package | Version | Purpose |
|---------|---------|---------|
| `llama-index-llms-llama-cpp` | Latest | Wrapper for llama.cpp execution |
| `llama-cpp-python` | Latest | Backing engine for GGUF execution on CPU |

## Ready for Planning
- [x] Questions answered
- [x] Approach selected
- [x] Dependencies identified
