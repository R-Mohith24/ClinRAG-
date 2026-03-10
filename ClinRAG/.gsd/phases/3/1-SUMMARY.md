# Wave 1 Summary – Plan 3.1

**Phase:** 3  
**Plan:** 1 (FastAPI Backend)  
**Status:** ✅ Complete

## What Was Done

### `requirements.txt` / Dependencies
- Installed `fastapi`, `uvicorn`, `streamlit`, `requests`.

### `src/api/main.py`
- Created FastAPI app `ClinRAG API`.
- Implemented `@asynccontextmanager` lifespan event to:
  - Initialize the BioMistral LLM.
  - Load the FAISS vector index from `data/llamaindex_storage`.
  - Build the `CitationQueryEngine` and the `CondenseQuestionChatEngine`.
  - Store the ChatEngine globally in `app_state` so it doesn't reload on every query.
- Created `GET /health` endpoint for readiness checks.
- Created `POST /chat` endpoint to receive medical queries.
- Extracted `response.response` for the text answer and parsed `response.source_nodes` into a clean JSON array of citations (id, test, score) to serve to the frontend.
