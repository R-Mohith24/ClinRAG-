---
phase: 3
plan: 2
wave: 2
---

# Plan 3.2: Streamlit UI

## Goal
Build `src/ui/app.py` to provide a chat interface with inline citations.

## Requirements Covered
- **REQ-05**: Extract and render formatted citations (Book, Page, Chapter) via a Streamlit UI component.

## Tasks

<task>
1. Update `requirements.txt` if not done in wave 1 (add `streamlit`, `requests`).
2. Create `src/ui/app.py`.
3. Set up the Streamlit page config (title: "ClinRAG Medical Assistant", icon: "⚕️").
4. Initialize `st.session_state.messages` to store chat history (`role`, `content`, `citations`).
5. Render existing messages in a `st.chat_message` loop.
   - For assistant messages, display the text, and if `citations` exist, display them in an `st.expander` or smaller text below.
6. Handle new user input via `if prompt := st.chat_input():`
   - Append user message to `st.session_state`.
   - Send `POST` request to `http://localhost:8000/chat`.
   - Parse the response (extract `answer` and `citations`).
   - Append assistant message to `st.session_state`.
   - Rerun or elegantly write to screen.
</task>

## Verification
<verify>
Run `streamlit run src/ui/app.py` while the FastAPI backend is running. Submit a medical question and visually verify that the citations appear under the answer.
</verify>
