"""
Query Engine Module
Wires the loaded FAISS index and the BioMistral LLM into a LlamaIndex QueryEngine.
"""

from llama_index.core import Settings, VectorStoreIndex
from src.ingestion.embedder import get_embedder


def build_query_engine(index: VectorStoreIndex, llm):
    """Build and return a RetrieverQueryEngine.

    - Applies the E5-Large embedder and BioMistral LLM to the global LlamaIndex Settings.
    - Returns a QueryEngine that retrieves the top-3 most relevant textbook chunks
      for each question, then uses BioMistral to compose the answer.

    Args:
        index: A VectorStoreIndex (loaded from the FAISS store built in Phase 1).
        llm:   A LlamaCPP instance (from src.llm.biomistral.get_llm).

    Returns:
        A QueryEngine ready to answer medical questions.
    """
    # Set global LlamaIndex settings so both retrieval and generation use the correct models
    Settings.llm = llm
    Settings.embed_model = get_embedder()

    # similarity_top_k=3 means: for each question, fetch the 3 most relevant passages
    query_engine = index.as_query_engine(similarity_top_k=3)
    return query_engine
