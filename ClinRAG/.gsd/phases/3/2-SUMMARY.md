# Wave 2 Summary – Plan 3.2

**Phase:** 3  
**Plan:** 2 (Streamlit UI with Citations)  
**Status:** ✅ Complete

## What Was Done

### `src/ui/app.py`
- Built a Streamlit chatbot interface connecting to the local FastAPI backend on port 8000.
- Implemented `st.session_state.messages` to maintain chat history and render previous turns.
- Used `requests.post()` to feed the `user_input` to the backend and parse standard JSON.
- **Citations Feature (REQ-05):** Added a `st.expander("🔍 View Source Citations")` natively under the bot's response to loop through and render medical textbook chunks exactly as they were retrieved by FAISS.

## Verification
- Run `uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &`
- Run `streamlit run src/ui/app.py`
- UI tested visually; error states (ConnectionRefused) gracefully handled.
