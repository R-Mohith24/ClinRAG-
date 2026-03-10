"""
BioMistral LLM Wrapper
Loads the 4-bit quantized BioMistral-7B GGUF model using llama-cpp for fast CPU inference.
"""

import os

from llama_index.llms.llama_cpp import LlamaCPP

DEFAULT_MODEL_PATH = "models/llm/biomistral-7b-Q4_K_M.gguf"


def get_llm(model_path: str = DEFAULT_MODEL_PATH) -> LlamaCPP:
    """Return a LlamaCPP instance configured for the BioMistral model.

    Args:
        model_path: Path to the local GGUF model file.

    Returns:
        LlamaCPP object ready for CPU inference.

    Raises:
        FileNotFoundError: If the GGUF model file is not present at model_path.
    """
    if not os.path.isfile(model_path):
        raise FileNotFoundError(
            f"\n[ERROR] BioMistral model not found at: '{model_path}'\n"
            f"Please download the 4-bit quantized GGUF file and place it at:\n"
            f"  {os.path.abspath(model_path)}\n"
            f"You can download it from HuggingFace:\n"
            f"  https://huggingface.co/BioMistral/BioMistral-7B-DARE-GGUF\n"
        )

    return LlamaCPP(
        model_path=model_path,
        temperature=0.1,       # Low temperature = more factual, less creative
        max_new_tokens=512,    # Keep answers concise for medical QA
        context_window=3900,   # How much text the model can "see" at once
        verbose=False,
    )
