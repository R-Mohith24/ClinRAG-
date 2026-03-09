---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: BioMistral LLM Wrapper & Base Query Engine

## Objective
Implement the quantized BioMistral-7B LLM instance using `llama.cpp` and wrap it into a standard base LlamaIndex Query Engine hooked into our FAISS index.

## Context
- .gsd/SPEC.md
- .gsd/ROADMAP.md
- .gsd/phases/2/RESEARCH.md

## Tasks

<task type="auto">
  <name>Create BioMistral Wrapper</name>
  <files>src/llm/biomistral.py</files>
  <action>
    Create a module that defines an initialization function `get_llm(model_path: str)`.
    - Use `LlamaCPP` from `llama_index.llms.llama_cpp`.
    - Set `model_path=model_path`, `temperature=0.1`, `max_new_tokens=512`.
    - In `model_kwargs`, set `n_ctx=3900` to allocate a sizable context window for retrieved documents.
    - Check if the model file explicitly exists at the path before instantiating, throwing an informative `FileNotFoundError` explicitly instructing the user to download the model into the `models/llm/` directory if absent.
  </action>
  <verify>python -c "from src.llm.biomistral import get_llm"</verify>
  <done>Returns a strictly configured local LlamaCPP instance.</done>
</task>

<task type="auto">
  <name>Create Base Query Engine</name>
  <files>src/rag/query_engine.py</files>
  <action>
    Create a module that binds the loaded FAISS index, the Embedder, and the BioMistral LLM together into a `RetrieverQueryEngine`.
    - Define a function `build_query_engine(index, llm)`.
    - Apply `Settings.llm = llm` and `Settings.embed_model = get_embedder()` inside the function.
    - Return `index.as_query_engine(similarity_top_k=3)`.
  </action>
  <verify>python -c "from src.rag.query_engine import build_query_engine"</verify>
  <done>Query engine accurately retrieves standard responses fetching the Top-3 context chunks.</done>
</task>

## Success Criteria
- [ ] Safe `FileNotFoundError` guard implemented in LLM wrapper.
- [ ] Base QueryEngine configured with $k=3$ Top Retrieval.
