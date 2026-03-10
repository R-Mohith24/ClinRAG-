"""
True Semantic Chunker Module
Splits LlamaIndex Document objects using advanced Semantic Breakpoints.
Instead of a fixed size, it analyzes the embedding similarity between sentences and cuts
the text ONLY when the topic changes natively, preventing information loss.
"""

from typing import List

from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.schema import BaseNode, Document
from src.ingestion.embedder import get_embedder


def chunk_documents(documents: List[Document]) -> List[BaseNode]:
    """
    Split documents into true semantic chunks.

    How it works for your project (IEEE level):
    1. It takes sentences from the textbook.
    2. It calculates the vector embedding for each sentence using our E5-Large-V2 model.
    3. It compares the cosine similarity between adjacent sentences.
    4. When similarity drops sharply (a 'breakpoint'), it means the topic changed.
    5. It cuts the chunk exactly at that natural boundary, ensuring high-quality RAG retrieval.

    Args:
        documents: List of LlamaIndex Document objects.

    Returns:
        List of BaseNode objects (dynamically sized text chunks bounded by topic).
    """
    if not documents:
        print("[WARNING] No documents provided for chunking. Returning empty list.")
        return []

    print(f"\n[INFO] Initializing Advanced Semantic Splitter using E5-Large-V2...")
    
    # We use the same powerful embedding model to analyze the text structure natively
    embed_model = get_embedder()
    
    splitter = SemanticSplitterNodeParser(
        buffer_size=1, 
        breakpoint_percentile_threshold=95, 
        embed_model=embed_model,
    )
    
    print(f"[INFO] Analyzing text for semantic breakpoints (topic changes)...")
    nodes = splitter.get_nodes_from_documents(documents)
    
    print(f"[INFO] Created {len(nodes)} dynamic semantic chunk(s) from {len(documents)} document(s).")
    return nodes
