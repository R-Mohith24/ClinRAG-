# DECISIONS.md

This file documents Architectural Decision Records (ADR).

## Phase 1 Decisions

**Date:** 2026-03-05

### Scope
- **Data Source:** Actual medical textbooks will be used directly; no temporary sample texts are needed.

### Approach
- **Modular Design:** Chose Option B. The system will be divided into `document_loader.py`, `chunker.py`, and `embedder.py` which are then composed inside `build_index.py`. This ensures better maintainability.
- **Dependency Management:** Chose Python's native `pip` and `venv` to align with the "Keep It Simple" methodology.
- **Data Preprocessing:** Relying primarily on `SimpleDirectoryReader`'s default behavior. Robust text cleaning (like Regex filtering of headers/footers) will be skipped initially and reconsidered later based on chunking tests.

### Constraints
- PDF Extraction might contain noise, but prioritizing modularity and testing core LlamaIndex first.
