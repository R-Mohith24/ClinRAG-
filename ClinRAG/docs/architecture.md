# ClinRAG — System Architecture

## Full Pipeline Diagram

```mermaid
flowchart TD
    subgraph OFFLINE["🔧 Offline Ingestion Pipeline (Phase 1)"]
        A["📄 Medical PDFs<br/>(Merck Manual)"] --> B["📖 Document Loader<br/>(SimpleDirectoryReader)"]
        B --> C["✂️ Semantic Chunker<br/>(SemanticSplitterNodeParser)"]
        C --> D["🧮 E5-Large-V2 Embedder<br/>(1024-dimensional vectors)"]
        D --> E["💾 FAISS Vector Index<br/>(IndexFlatIP, persisted)"]
    end

    subgraph ONLINE["⚡ Online Query Pipeline (Phase 2-3)"]
        F["👤 User Question"] --> G["🌐 Streamlit UI<br/>(Chat Interface)"]
        G -->|"HTTP POST /chat"| H["⚙️ FastAPI Backend"]
        H --> I["🔍 CitationQueryEngine<br/>(top-k=3 retrieval)"]
        I --> E
        I --> J["🧠 BioMistral-7B<br/>(4-bit GGUF, CPU)"]
        J --> K["📝 Answer + Citations<br/>([1], [2], [3])"]
        K --> H
        H -->|"JSON Response"| G
        G --> L["💬 Chat Display<br/>+ Expandable Citations"]
    end

    subgraph MEMORY["🧠 Conversation Memory"]
        H --> M["♻️ CondenseQuestionChatEngine<br/>(CRC Pattern)"]
        M --> N["📋 ChatMemoryBuffer<br/>(1500 tokens)"]
    end

    subgraph EVAL["📊 Evaluation Pipeline (Phase 4)"]
        O["📝 50 Test Queries<br/>(test_qa.json)"] --> P["⏱️ generate_dataset.py<br/>(latency tracking)"]
        P --> I
        P --> Q["📦 eval_results.json"]
        Q --> R["🏆 run_ragas.py<br/>(Local BioMistral Judge)"]
        R --> S["📊 ragas_report.csv<br/>(Faithfulness, Relevancy)"]
    end

    style OFFLINE fill:#e8f5e9,stroke:#2e7d32
    style ONLINE fill:#e3f2fd,stroke:#1565c0
    style MEMORY fill:#fff3e0,stroke:#ef6c00
    style EVAL fill:#fce4ec,stroke:#c62828
```

## Component Descriptions

| Component | Module | Purpose |
|-----------|--------|---------|
| Document Loader | `src/ingestion/document_loader.py` | Reads PDF files using LlamaIndex's `SimpleDirectoryReader` |
| Semantic Chunker | `src/ingestion/chunker.py` | Splits text at natural topic boundaries using embedding similarity |
| Embedder | `src/ingestion/embedder.py` | Generates 1024-dim vectors using `intfloat/e5-large-v2` |
| Index Builder | `src/ingestion/build_index.py` | Orchestrates ingestion and persists FAISS index |
| BioMistral LLM | `src/llm/biomistral.py` | 4-bit quantized medical LLM via `llama-cpp` |
| Citation Query Engine | `src/rag/query_engine.py` | Retrieves top-3 passages and injects inline `[1][2][3]` citations |
| Chat Engine | `src/rag/chat_engine.py` | Condense-Rephrase-Chat pattern with 1500-token memory |
| FastAPI Backend | `src/api/main.py` | REST API loading the full pipeline once on startup |
| Streamlit UI | `src/ui/app.py` | Chat interface with expandable citation dropdowns |
| Dataset Generator | `src/eval/generate_dataset.py` | Runs test queries, records latency and citations |
| RAGAS Evaluator | `src/eval/run_ragas.py` | Offline Faithfulness and Answer Relevancy grading |

## Data Flow Summary

1. **Offline**: PDFs → Semantic Chunks → E5 Embeddings → FAISS Index (stored on disk)
2. **Online**: User Question → FastAPI → Retrieve Top-3 Chunks → BioMistral generates Answer with Citations → Streamlit displays Answer + Citation Expander
3. **Evaluation**: 50 Test Questions → Pipeline → RAGAS grades Faithfulness & Relevancy → CSV Report
