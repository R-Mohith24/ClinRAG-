---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Document Loading and Chunking

## Objective
Implement modular data loading and semantic chunking using LlamaIndex's `SimpleDirectoryReader` and `SentenceSplitter`. This addresses the first half of Phase 1 requirements, moving raw PDFs into processable chunks (nodes).

## Context
- .gsd/SPEC.md
- .gsd/ROADMAP.md
- .gsd/phases/1/RESEARCH.md

## Tasks

<task type="auto">
  <name>Create Document Loader</name>
  <files>src/ingestion/document_loader.py</files>
  <action>
    Create a module that defines a function `load_documents(input_dir: str)` -> `List[Document]`.
    - Use LlamaIndex's `SimpleDirectoryReader` to load data from `input_dir`.
    - Handle potential `ValueError` if the directory is empty or missing, printing a useful warning.
    - Avoid hardcoding directories directly in the function body; pass `input_dir` as an argument.
  </action>
  <verify>python -c "from src.ingestion.document_loader import load_documents"</verify>
  <done>Function successfully loads testing PDFs (or gracefully returns empty list if directory missing) without syntax errors.</done>
</task>

<task type="auto">
  <name>Create Semantic Chunker</name>
  <files>src/ingestion/chunker.py</files>
  <action>
    Create a module that defines a function `chunk_documents(documents: List[Document])` -> `List[BaseNode]`.
    - Instantiate LlamaIndex `SentenceSplitter` with `chunk_size=512` and `chunk_overlap=50`.afile
    - Call the splitter's `get_nodes_from_documents(documents)` method.
    - Return the resulting nodes.
  </action>
  <verify>python -c "from src.ingestion.chunker import chunk_documents"</verify>
  <done>Function successfully parses typical document structures into chunk nodes based on the 512 size configuration.</done>
</task>

## Success Criteria
- [ ] `document_loader.py` securely imports and handles SimpleDirectoryReader.
- [ ] `chunker.py` correctly uses SentenceSplitter to create node chunks of size 512 with overlap 50.
