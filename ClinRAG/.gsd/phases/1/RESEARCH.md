---
phase: 1
level: 2
researched_at: 2026-03-05
---

# Phase 1 Research

## Questions Investigated
1. How best to cleanly separate ingestion tasks (`document_loader.py`, `chunker.py`, `embedder.py`) into LlamaIndex's pipeline architecture seamlessly?
2. What are the specific hyperparameter requirements for `intfloat/e5-large-v2` in LlamaIndex Context (Embedding dimensions, Query prefix)?
3. How to initialize and properly persist a local FAISS index within LlamaIndex so `build_index.py` stores it exactly at `data/llamaindex_storage/`?

## Findings

### Modular Loading & Processing in LlamaIndex
LlamaIndex typically uses a single `VectorStoreIndex.from_documents` method, but under the hood, we can manually parse documents into nodes (chunks) using an `IngestionPipeline` or explicit `SentenceSplitter`.
**Recommendation:** We can write:
- `document_loader.py`: Expose a function returning `List[Document]` using `SimpleDirectoryReader(input_dir).load_data()`.
- `chunker.py`: Use `SentenceSplitter(chunk_size=512, chunk_overlap=50)` over the document list to retrieve `List[BaseNode]`.
- `embedder.py`: Utilize `HuggingFaceEmbedding(model_name="intfloat/e5-large-v2")` to attach an embedding array onto nodes or let the index automatically do this.

### E5-Large V2 Embedding Quirks
The `intfloat/e5-large-v2` generates 1024-dimensional floating point embeddings. It traditionally demands "query: " to be prepended to queries, and "passage: " prepended to raw text passages. LlamaIndex’s `HuggingFaceEmbedding` conveniently covers these arguments inherently using `query_instruction` and `text_instruction`.
**Recommendation:** Instantiate `faiss.IndexFlatIP(1024)` due to E5 output dimension sizes, and define appropriate `HuggingFaceEmbedding` parameters.

### Persisting FAISS Index with LlamaIndex
To persist a local FAISS index, LlamaIndex expects a `StorageContext` object instantiated with a `FaissVectorStore`.
**Recommendation:**
```python
faiss_index = faiss.IndexFlatL2(1024)
vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
index.storage_context.persist(persist_dir="data/llamaindex_storage/")
```

## Decisions Made
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Architecture Workflow | Manual Node Extractor -> VectorIndex | Explicit chunking with `SentenceSplitter` gives the most clarity & adheres to our strict modular separation approach. |
| FAISS Distance Metric | L2 Distance / Inner Product | Inner Product (Cosine similarity when normalized) perfectly complements E5-Large style embeddings. Dimension configured to 1024. |

## Patterns to Follow
- Construct the `StorageContext` fully initialized before running document ingestion.
- Pre-pass node chunks (`List[TextNode]`) generated from `SentenceSplitter` to `VectorStoreIndex(nodes=...)` rather than directly `from_documents()` to ensure our modular `chunker.py` gets the responsibility.

## Anti-Patterns to Avoid
- Don't construct a `VectorStoreIndex` with default simple embeddings. Be sure to configure the Service Context / Settings with our custom `intfloat/e5-large-v2` embedder to avoid sending requests to OpenAI default APIs!

## Dependencies Identified
| Package | Version | Purpose |
|---------|---------|---------|
| `llama-index-core` | Latest | Core indexing utility |
| `llama-index-readers-file` | Latest | For `SimpleDirectoryReader` local PDF extraction |
| `llama-index-embeddings-huggingface`| Latest | Embeddings through E5 |
| `llama-index-vector-stores-faiss`| Latest | FAISS local indexing |
| `faiss-cpu` | Latest | Hardware logic |

## Risks
- Download time: E5 model might stall pipeline execution internally the first time; mitigation is downloading inside a Jupyter/notebook first or being patient.
- Faulty PDFs stalling SimpleDirectoryReader: mitigate by wrapping load loops cleanly.

## Ready for Planning
- [x] Questions answered
- [x] Approach selected
- [x] Dependencies identified
