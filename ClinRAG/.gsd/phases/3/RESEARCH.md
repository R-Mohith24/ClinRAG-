# Phase 3 Research Insights

## Objective
Build the Application Layer (Phase 3) for ClinRAG.
This requires exposing the RAG pipeline over a FastAPI backend (REQ-06) and building a chat-like Streamlit frontend that renders citations (REQ-05).

## 1. FastAPI Backend
We need an API that acts as the bridge between the UI and our heavy RAG pipeline. Loading the BioMistral model takes time and memory, so it should be loaded once at startup in the API, not on every Streamlit script execution.

**Endpoints needed:**
- `GET /health` : Returns API status.
- `POST /chat` : Accepts a user message and a session_id, returns the generated answer and associated citations.

**State Management:**
Since it's a multi-turn chat, the backend needs to orchestrate the ChatEngine. However, LlamaIndex's `CondenseQuestionChatEngine` maintains its own `ChatMemoryBuffer`. If we have multiple concurrent users (or just want to be statelessREST), we might need an engine-per-session factory, OR we maintain one global engine for the local MVP. Given this is a local setup for an IEEE presentation, a single global `chat_engine` instantiated on server startup is sufficient and highly efficient.

## 2. Handling Citations in LlamaIndex
In Phase 2, we used `CitationQueryEngine`.
When we call `chat_engine.chat("user message")`, it returns a response object.
- `response.response`: The generated text, which includes inline citation markers like `[1]`, `[2]`.
- `response.source_nodes`: A list of `NodeWithScore` objects. These correspond exactly to the citations. `source_nodes[0]` is citation `[1]`, `source_nodes[1]` is `[2]`, etc.

To send this cleanly over REST, our FastAPI `/chat` endpoint should return:
```json
{
  "answer": "Diabetes is a chronic disease [1]. It involves insulin resistance [2].",
  "citations": [
    {"id": 1, "text": "Diabetes mellitus is a metabolic..."},
    {"id": 2, "text": "Type 2 diabetes is characterized by insulin resistance..."}
  ]
}
```

## 3. Streamlit Frontend
Streamlit natively supports chatbots via `st.chat_message` and `st.chat_input`.
The frontend will:
1. Maintain `st.session_state.messages` to visually render the chat history.
2. Send the latest user input to the FastAPI `/chat` endpoint via `requests.post`.
3. Display the assistant's answer.
4. Render the citations gracefully (e.g., using Streamlit `st.expander` or markdown footers) beneath the answer.

## Libraries Needed
- `fastapi`
- `uvicorn`
- `streamlit`
- `requests`

*These need to be added to `requirements.txt`*
