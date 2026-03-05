---
phase: 1
plan: 2
wave: 2
---

# Plan 1.2: Embedding and FAISS Storage

## Objective
Configure the E5-Large HuggingFace embedding utility within LlamaIndex, connect it to a FAISS vector index, and wrap the ingestion pipeline inside `build_index.py`. This step finalizes Phase 1 by resulting in persistent FAISS storage metadata.

## Context
- .gsd/ROADMAP.md
- .gsd/phases/1/RESEARCH.md
- .gsd/SPEC.md

## Tasks

<task type="auto">
  <name>Create Embedder Configuration Module</name>
  <files>src/ingestion/embedder.py</files>
  <action>
    Create a module that defines a function `get_embedder()`.
    - Instantiate and return `HuggingFaceEmbedding(model_name="intfloat/e5-large-v2")`.
    - No direct index processing happens here—just returning the configured `embedder` object for LlamaIndex to use in the global settings.
  </action>
  <verify>python -c "from src.ingestion.embedder import get_embedder"</verify>
  <done>Returns a valid initialized LlamaIndex Embedding instance representing E5-Large.</done>
</task>

<task type="auto">
  <name>Create Index Builder (Builds FAISS DB)</name>
  <files>src/ingestion/build_index.py</files>
  <action>
    Create the main orchestrator script that relies on `document_loader.py`, `chunker.py`, and `embedder.py`.
    - Define a `main()` function:
    - Step 1: Assign `Settings.embed_model = get_embedder()`.
    - Step 2: Use `load_documents("data/raw_pdfs")`.
    - Step 3: Transform to raw chunks using `chunk_documents(documents)`.
    - Step 4: Create a Faiss 1024-dimension Index `faiss.IndexFlatIP(1024)`.
    - Step 5: Wrap it using `FaissVectorStore(faiss_index=faiss_index)` and `StorageContext.from_defaults(vector_store=vector_store)`.
    - Step 6: Construct the Index using `VectorStoreIndex(nodes=nodes, storage_context=storage_context)`.
    - Step 7: Save to disk using `index.storage_context.persist(persist_dir="data/llamaindex_storage/")`.
    - Step 8: Ensure directories `data/raw_pdfs` and `data/llamaindex_storage` are handled.
    - Write a standard `if __name__ == "__main__":` block to run `main()`.
  </action>
  <verify>python -c "from src.ingestion.build_index import main"</verify>
  <done>The pipeline orchestration is defined sequentially and can programmatically process input to store FAISS data inside `.json` stores.</done>
</task>

## Success Criteria
- [ ] Correctly integrates Faiss inner product distances scaled to dimensions of 1024.
- [ ] Successfully stores index structures (e.g. `docstore.json`, `index_store.json`) at `data/llamaindex_storage/`.
- [ ] Connects modular code paths.
