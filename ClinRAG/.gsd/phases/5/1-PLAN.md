---
phase: 5
plan: 1
wave: 1
---

# Plan 5.1: README & Architecture Documentation

## Objective
Create a professional README.md and an architecture diagram document so the project looks polished for GitHub and faculty review.

## Tasks

<task type="auto">
  <name>Create Professional README.md</name>
  <files>
    - README.md
  </files>
  <action>
    - Write a comprehensive README with:
      - Project title, badges, and one-liner description.
      - Features list (Semantic Chunking, CitationQueryEngine, Offline RAGAS, etc.)
      - Architecture overview (embed the Mermaid diagram).
      - Prerequisites and Installation steps.
      - Usage instructions (how to run ingestion, API, and UI).
      - Project structure tree.
      - Tech stack table.
      - License section.
  </action>
  <verify>cat README.md | head -50</verify>
  <done>README.md exists with all sections populated.</done>
</task>

<task type="auto">
  <name>Create Architecture Diagram</name>
  <files>
    - docs/architecture.md
  </files>
  <action>
    - Create a Mermaid flowchart showing the full ClinRAG pipeline:
      - PDF Ingestion → Semantic Chunker → E5-Large-V2 Embeddings → FAISS Index
      - User Query → FastAPI → CitationQueryEngine → BioMistral → Response + Citations
      - Streamlit UI ↔ FastAPI Backend
    - Add a brief written explanation of each component.
  </action>
  <verify>cat docs/architecture.md</verify>
  <done>Architecture diagram renders correctly in Markdown preview.</done>
</task>

## Success Criteria
- [ ] README.md is professional and complete.
- [ ] Architecture diagram clearly shows the full data flow.
