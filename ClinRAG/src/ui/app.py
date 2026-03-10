"""
ClinRAG - Streamlit UI
Interactive chat interface for the medical RAG assistant.
Communicates with the FastAPI backend over HTTP to keep the frontend lightweight.
Renders inline citations beautifully using Streamlit UI components.
"""

import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

# --- Page Setup ---
st.set_page_config(
    page_title="ClinRAG Assistant",
    page_icon="⚕️",
    layout="centered"
)


# --- Custom Styling (Aesthetics) ---
st.markdown("""
<style>
/* Medical-themed header styling */
.main-header {
    text-align: center;
    color: #2e6c80;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.sub-header {
    text-align: center;
    color: #555;
    font-size: 1.1em;
    margin-bottom: 2rem;
}
/* Citation styling */
.citation-box {
    background-color: #f8f9fa;
    border-left: 4px solid #0056b3;
    padding: 10px;
    margin-top: 5px;
    margin-bottom: 10px;
    border-radius: 4px;
    font-size: 0.9em;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>⚕️ ClinRAG Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Hallucination-Free Medical QA with Source Citations</p>", unsafe_allow_html=True)


# --- State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am ClinRAG, your medical AI assistant powered by the Merck Manual. How can I help you today?", "citations": []}
    ]


# --- Render Conversation History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
        # Render citations if they exist for this message
        if msg.get("citations"):
            with st.expander("🔍 View Source Citations"):
                for cit in msg["citations"]:
                    st.markdown(f"**[{cit['id']}] (Score: {cit['score']})**")
                    st.markdown(f"<div class='citation-box'>{cit['text']}</div>", unsafe_allow_html=True)


# --- Handle User Input ---
user_input = st.chat_input("Ask a medical question (e.g., 'What are the symptoms of type 2 diabetes?')...")

if user_input:
    # Immediately render the user's message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Store into state
    st.session_state.messages.append({"role": "user", "content": user_input, "citations": []})
    
    # Show loading spinner while requesting from backend
    with st.chat_message("assistant"):
        with st.spinner("Analyzing medical texts and generating answer..."):
            try:
                # Call FastAPI backend
                response = requests.post(API_URL, json={"message": user_input})
                response.raise_for_status()  # Check for HTTP errors
                
                data = response.json()
                answer = data.get("answer", "No answer received.")
                citations = data.get("citations", [])
                
                # Write the answer back to the UI
                st.write(answer)
                
                # Write the citations immediately below the answer
                if citations:
                    with st.expander("🔍 View Source Citations"):
                        for cit in citations:
                            st.markdown(f"**[{cit['id']}] (Score: {cit['score']})**")
                            st.markdown(f"<div class='citation-box'>{cit['text']}</div>", unsafe_allow_html=True)
                
                # Save assistant's answer and citations into state
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "citations": citations
                })
                
            except requests.exceptions.ConnectionError:
                error_msg = "❌ Connection Error: The ClinRAG backend is not running. Please start the FastAPI server first."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg, "citations": []})
            except Exception as e:
                error_msg = f"❌ An error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg, "citations": []})
