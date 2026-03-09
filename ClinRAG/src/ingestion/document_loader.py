"""
Document Loader Module
Loads medical textbook PDFs from a specified directory using LlamaIndex's SimpleDirectoryReader.
"""

import os
from typing import List

from llama_index.core.schema import Document
from llama_index.readers.file import SimpleDirectoryReader


def load_documents(input_dir: str) -> List[Document]:
    """
    Load all documents from the given directory.

    Args:
        input_dir: Path to the directory containing PDF files.

    Returns:
        List of LlamaIndex Document objects with text and metadata.
    """
    if not os.path.isdir(input_dir):
        print(f"[WARNING] Directory '{input_dir}' does not exist. Returning empty list.")
        return []

    if not os.listdir(input_dir):
        print(f"[WARNING] Directory '{input_dir}' is empty. Returning empty list.")
        return []

    try:
        reader = SimpleDirectoryReader(input_dir=input_dir)
        documents = reader.load_data()
        print(f"[INFO] Loaded {len(documents)} document(s) from '{input_dir}'.")
        return documents
    except ValueError as e:
        print(f"[ERROR] Failed to load documents from '{input_dir}': {e}")
        return []
