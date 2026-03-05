# ROADMAP.md

> **Current Phase**: Not started
> **Milestone**: v1.0

## Must-Haves (from SPEC)
- [ ] Offline Pre-processing pipeline (PDF extraction, embedding, FAISS vector DB).
- [ ] Online interaction pipeline (API + Streamlit + LlamaIndex CRC memory).
- [ ] Low-latency CPU inference via BioMistral 4-bit and llama.cpp.
- [ ] Evaluation system generating RAGAS metrics, Hallucination Reduction, and latency details. 

## Phases

### Phase 1: Setup & Index Creation
**Status**: ⬜ Not Started
**Objective**: Develop script to load PDFs, chunk text safely, embed via E5-Large, and build FAISS index locally.
**Requirements**: REQ-01, REQ-02

### Phase 2: RAG Pipeline
**Status**: ⬜ Not Started
**Objective**: Combine BioMistral LLM wrapper, Query Engine, and Multi-turn Chat Engine with memory context.
**Requirements**: REQ-03, REQ-04

### Phase 3: Application Layer
**Status**: ⬜ Not Started
**Objective**: Expose the logic on FastApi and present interactions with citations in a chat-style Streamlit webapp.
**Requirements**: REQ-05, REQ-06

### Phase 4: Evaluation
**Status**: ⬜ Not Started
**Objective**: Process 50 query-datasets comparing RAG against No-RAG baselines, calculating Hallucinations vs True Mentions, and speed analysis.
**Requirements**: REQ-07, REQ-08

### Phase 5: Documentation & Presentation
**Status**: ⬜ Not Started
**Objective**: Finalize draft of IEEE Research Paper, Evaluation Charts, slide decks, and Demo screenshots/videos.
