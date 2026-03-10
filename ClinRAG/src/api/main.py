"""
ClinRAG - FastAPI Backend
Provides a robust REST API for the ClinRAG medical assistant.
Loads the BioMistral ChatEngine once on startup to ensure fast, responsive queries.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_index.core import StorageContext, load_index_from_storage

from src.llm.biomistral import get_llm
from src.rag.query_engine import build_query_engine
from src.rag.chat_engine import build_chat_engine

# Global state to hold the engine
app_state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for FastAPI.
    Runs exactly once when the server starts up.
    Loads the LLM, the FAISS index, and builds the ChatEngine.
    """
    print("="*50)
    print("Initializing ClinRAG Backend...")
    print("="*50)
    
    try:
        # 1. Load the LLM
        print("[INFO] Loading BioMistral LLM...")
        llm = get_llm()
        
        # 2. Load the pre-built FAISS index
        print("[INFO] Loading FAISS index from 'data/llamaindex_storage'...")
        storage_context = StorageContext.from_defaults(persist_dir="data/llamaindex_storage")
        index = load_index_from_storage(storage_context)
        
        # 3. Build the engines
        print("[INFO] Building Query Engine (with Citations)...")
        query_engine = build_query_engine(index, llm)
        
        print("[INFO] Building Conversational Chat Engine...")
        chat_engine = build_chat_engine(query_engine)
        
        # Store globally
        app_state["chat_engine"] = chat_engine
        print("✅ Backend ready to accept requests.")
        
    except Exception as e:
        print(f"❌ Failed to initialize backend: {e}")
        raise e
        
    yield  # Server runs here
    
    # Cleanup (if any) goes here when server shuts down
    app_state.clear()


# Initialize the FastAPI app
app = FastAPI(
    title="ClinRAG API",
    description="Backend for the Hallucination-Free Medical RAG Chatbot",
    version="1.0.0",
    lifespan=lifespan
)


# --- Request/Response Models ---

class ChatRequest(BaseModel):
    message: str

class CitationModel(BaseModel):
    id: int
    text: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    citations: list[CitationModel]


# --- Endpoints ---

@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "engine_loaded": "chat_engine" in app_state}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint.
    Takes a user's message, generates a response using the RAG pipeline,
    and cleanly extracts source citations for the UI to display.
    """
    engine = app_state.get("chat_engine")
    if not engine:
        raise HTTPException(status_code=503, detail="Chat engine not ready yet.")
        
    print(f"\n[USER] {request.message}")
    
    try:
        # Get response from the LlamaIndex ChatEngine
        response = engine.chat(request.message)
        
        # Extract the pure text answer
        answer_text = str(response.response)
        
        # Extract the source nodes (citations) used to generate the answer
        citations = []
        if response.source_nodes:
            for idx, node_with_score in enumerate(response.source_nodes, start=1):
                citations.append({
                    "id": idx,
                    "text": node_with_score.node.get_content().strip(),
                    "score": round(node_with_score.score, 4) if node_with_score.score else 0.0
                })
                
        return {
            "answer": answer_text,
            "citations": citations
        }
        
    except Exception as e:
        print(f"[ERROR] Chat generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
