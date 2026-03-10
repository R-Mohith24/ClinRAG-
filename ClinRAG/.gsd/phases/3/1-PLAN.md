---
phase: 3
plan: 1
wave: 1
---

# Plan 3.1: FastAPI Backend

## Goal
Build `src/api/main.py` to expose the ClinRAG pipeline over a REST API.

## Requirements Covered
- **REQ-06**: Expose endpoints for queries and session management through a FastAPI Backend.

## Tasks

<task>
1. Update `requirements.txt` to include `fastapi`, `uvicorn`, and `requests`.
2. Create `src/api/main.py`.
3. Implement FastAPI app initialization.
   - Use `@app.on_event("startup")` to load the FAISS index, initialize the BioMistral LLM, and build the global `ChatEngine`.
4. Create a Pydantic model for the request body (`ChatRequest`: contains `message` str).
5. Create the `POST /chat` endpoint.
   - Call `chat_engine.chat(request.message)`.
   - Extract `.response` as the answer.
   - Extract `.source_nodes` into a structured list of citations (mapping index+1 to the node text/metadata).
   - Return structured JSON.
</task>

## Verification
<verify>
Run the API locally using `uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &`, then test the `/health` and `/chat` endpoints using `curl`.
</verify>
