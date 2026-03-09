"""
Semantic Chunker Module
Splits LlamaIndex Document objects into smaller, semantically coherent text nodes
using SentenceSplitter with configurable chunk size and overlap.
"""

from typing import List

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import BaseNode, Document


def chunk_documents(
    documents: List[Document],
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> List[BaseNode]:
    """
    Split documents into semantic chunks (nodes).

    Args:
        documents: List of LlamaIndex Document objects to chunk.
        chunk_size: Maximum number of tokens per chunk (default 512).
        chunk_overlap: Number of overlapping tokens between chunks (default 50).

    Returns:
        List of BaseNode objects (text chunks with metadata preserved).
    """
    if not documents:
        print("[WARNING] No documents provided for chunking. Returning empty list.")
        return []

    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    nodes = splitter.get_nodes_from_documents(documents)
    print(f"[INFO] Created {len(nodes)} chunk(s) from {len(documents)} document(s).")
    return nodes
