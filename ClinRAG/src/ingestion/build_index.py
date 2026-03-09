"""
Index Builder — Main Orchestrator
Composes document_loader, chunker, and embedder modules to build and persist
a FAISS vector index from medical textbook PDFs.
"""

import os
import sys

import faiss
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore

from src.ingestion.document_loader import load_documents
from src.ingestion.chunker import chunk_documents
from src.ingestion.embedder import get_embedder

# --- Configuration ---
RAW_PDFS_DIR = os.path.join("data", "raw_pdfs")
PERSIST_DIR = os.path.join("data", "llamaindex_storage")
EMBEDDING_DIM = 1024  # E5-Large-V2 output dimension


def main():
    """
    End-to-end ingestion pipeline:
    1. Configure embedding model
    2. Load PDFs from data/raw_pdfs/
    3. Chunk documents into semantic nodes
    4. Build FAISS index and persist to disk
    """
    # Step 1: Set global embedding model
    print("=" * 60)
    print("ClinRAG — Index Builder")
    print("=" * 60)

    embed_model = get_embedder()
    Settings.embed_model = embed_model

    # Step 2: Load documents
    print(f"\n[STEP 2] Loading documents from '{RAW_PDFS_DIR}'...")
    documents = load_documents(RAW_PDFS_DIR)
    if not documents:
        print("[ERROR] No documents loaded. Exiting.")
        sys.exit(1)

    # Step 3: Chunk documents
    print(f"\n[STEP 3] Chunking {len(documents)} document(s)...")
    nodes = chunk_documents(documents)
    if not nodes:
        print("[ERROR] No chunks created. Exiting.")
        sys.exit(1)

    # Step 4: Create FAISS index
    print(f"\n[STEP 4] Creating FAISS index (dim={EMBEDDING_DIM})...")
    faiss_index = faiss.IndexFlatIP(EMBEDDING_DIM)
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Step 5: Build VectorStoreIndex (embeds nodes automatically)
    print("\n[STEP 5] Building VectorStoreIndex (this may take a while)...")
    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
    )

    # Step 6: Persist to disk
    os.makedirs(PERSIST_DIR, exist_ok=True)
    print(f"\n[STEP 6] Persisting index to '{PERSIST_DIR}'...")
    index.storage_context.persist(persist_dir=PERSIST_DIR)

    print("\n" + "=" * 60)
    print(f"✅ Index built successfully!")
    print(f"   Documents loaded : {len(documents)}")
    print(f"   Chunks created   : {len(nodes)}")
    print(f"   Storage location : {PERSIST_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
