"""
Query Engine Module
Wires the loaded FAISS index and the BioMistral LLM into a LlamaIndex QueryEngine.
Uses a CitationQueryEngine to automatically inject source citations into answers.
"""

from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.query_engine import CitationQueryEngine
from src.ingestion.embedder import get_embedder


def build_query_engine(index: VectorStoreIndex, llm):
    """Build and return a CitationQueryEngine.

    - Applies the E5-Large embedder and BioMistral LLM to the global LlamaIndex Settings.
    - Uses LlamaIndex's built-in CitationQueryEngine so that the generated answers 
      include inline citations (e.g., [1], [2]) pointing directly to the source medical text.
    - Retrieves the top-3 most relevant textbook chunks for each question.

    Args:
        index: A VectorStoreIndex (loaded from the FAISS store built in Phase 1).
        llm:   A LlamaCPP instance (from src.llm.biomistral.get_llm).

    Returns:
        A CitationQueryEngine ready to answer medical questions with citations.
    """
    # Set global LlamaIndex settings so both retrieval and generation use the correct models
    Settings.llm = llm
    Settings.embed_model = get_embedder()

    # Create the CitationQueryEngine
    # similarity_top_k=3 means: for each question, fetch the 3 most relevant passages
    # citation_chunk_size controls how large the citation snippets are
    query_engine = CitationQueryEngine.from_args(
        index,
        similarity_top_k=3,
        citation_chunk_size=512,
    )
    return query_engine
