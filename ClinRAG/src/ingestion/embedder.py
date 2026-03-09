"""
Embedder Configuration Module
Returns a configured HuggingFace E5-Large-V2 embedding model for LlamaIndex.
"""

from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def get_embedder() -> HuggingFaceEmbedding:
    """
    Create and return the E5-Large-V2 embedding model.

    The model produces 1024-dimensional vectors optimized for semantic retrieval.
    LlamaIndex's HuggingFaceEmbedding handles the required query/passage prefixes
    automatically via query_instruction and text_instruction.

    Returns:
        Configured HuggingFaceEmbedding instance.
    """
    embed_model = HuggingFaceEmbedding(
        model_name="intfloat/e5-large-v2",
        query_instruction="query: ",
        text_instruction="passage: ",
    )
    print("[INFO] E5-Large-V2 embedding model initialized.")
    return embed_model
