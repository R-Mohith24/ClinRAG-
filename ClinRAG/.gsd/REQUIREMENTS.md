# REQUIREMENTS.md

## Format
| ID | Requirement | Source | Status |
|----|-------------|--------|--------|
| REQ-01 | Automatically load and chunk text from PDFs ensuring context preservation using LlamaIndex. | SPEC goal 4 | Pending |
| REQ-02 | Embed chunks into a FAISS local vector index with metadata using E5-Large. | SPEC goal 4 | Pending |
| REQ-03 | Retrieve Top-3 context intelligently across multi-turn interactions with Conversational Retrieval. | SPEC goal 4 | Pending |
| REQ-04 | Generate coherent context-only responses using BioMistral-7B 4-bit via llama.cpp. | SPEC goal 2 | Pending |
| REQ-05 | Extract and render formatted citations (Book, Page, Chapter) via a Streamlit UI component. | SPEC goal 1 | Pending |
| REQ-06 | Expose endpoints for queries and session management through a FastAPI Backend. | SPEC goal 4 | Pending |
| REQ-07 | Evaluate outputs from 50 test queries across RAGAS frameworks (Faithfulness/Answer Relevance). | SPEC goal 3 | Pending |
| REQ-08 | Generate an A/B latency and hallucination reduction comparison script on identical test queries. | SPEC goal 3 | Pending |
