# ⚕️ ClinRAG — Hallucination-Free Medical Question Answering

> A Retrieval-Augmented Generation (RAG) chatbot for clinical medicine, powered by BioMistral-7B and FAISS, with inline source citations and offline RAGAS evaluation.

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![LlamaIndex](https://img.shields.io/badge/LlamaIndex-RAG-orange.svg)](https://www.llamaindex.ai/)
[![BioMistral](https://img.shields.io/badge/LLM-BioMistral--7B-green.svg)](https://huggingface.co/BioMistral)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Semantic Chunking** | Splits medical text at natural topic boundaries using `SemanticSplitterNodeParser` |
| 📎 **Inline Citations** | Every answer includes `[1]`, `[2]`, `[3]` citations mapped to exact textbook passages |
| 🏥 **BioMistral-7B** | Domain-specific medical LLM running locally via 4-bit quantization (no GPU needed) |
| 🔍 **FAISS Vector Search** | Sub-millisecond semantic retrieval across thousands of medical text chunks |
| 💬 **Multi-turn Chat** | Conversational memory (CRC pattern) remembers follow-up questions naturally |
| 📊 **Offline RAGAS Evaluation** | Measures Faithfulness (hallucination) and Answer Relevancy without any API keys |
| 🖥️ **Streamlit UI** | Clean medical chat interface with expandable "View Source Citations" dropdowns |
| ⚡ **FastAPI Backend** | Persistent API server that loads the LLM once and serves queries instantly |

---

## 🏗️ Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Medical     │────▶│  Semantic        │────▶│  E5-Large-V2     │
│  PDFs        │     │  Chunker         │     │  Embeddings      │
└──────────────┘     └──────────────────┘     └────────┬─────────┘
                                                       │
                                                       ▼
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Streamlit   │◀───▶│  FastAPI         │────▶│  FAISS           │
│  Chat UI     │     │  Backend         │     │  Vector Index    │
└──────────────┘     └────────┬─────────┘     └──────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │  BioMistral-7B   │
                     │  (4-bit, CPU)    │
                     │  + Citations     │
                     └──────────────────┘
```

For the full Mermaid diagram, see [docs/architecture.md](docs/architecture.md).

---

## 📂 Project Structure

```
ClinRAG/
├── src/
│   ├── ingestion/
│   │   ├── document_loader.py   # PDF loading via LlamaIndex
│   │   ├── chunker.py           # SemanticSplitterNodeParser
│   │   ├── embedder.py          # E5-Large-V2 (1024-dim)
│   │   └── build_index.py       # End-to-end FAISS index builder
│   ├── llm/
│   │   └── biomistral.py        # BioMistral-7B GGUF wrapper
│   ├── rag/
│   │   ├── query_engine.py      # CitationQueryEngine (top-k=3)
│   │   └── chat_engine.py       # CondenseQuestionChatEngine + memory
│   ├── api/
│   │   └── main.py              # FastAPI backend
│   ├── ui/
│   │   └── app.py               # Streamlit chat interface
│   └── eval/
│       ├── generate_dataset.py  # Test query runner with latency tracking
│       └── run_ragas.py         # Offline RAGAS evaluation
├── data/
│   ├── raw_pdfs/                # Place medical textbook PDFs here
│   ├── llamaindex_storage/      # Persisted FAISS index
│   ├── test_qa.json             # Test questions + ground truths
│   └── eval_results.json        # Generated evaluation data
├── models/
│   └── llm/                     # Place BioMistral GGUF model here
├── docs/
│   ├── architecture.md          # System architecture diagram
│   └── ieee_paper_outline.md    # IEEE research paper draft
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Embedding | `intfloat/e5-large-v2` | 1024-dim semantic vectors |
| Vector DB | FAISS (IndexFlatIP) | Similarity search |
| LLM | BioMistral-7B Q4_K_M | Medical text generation |
| Framework | LlamaIndex | RAG orchestration |
| Backend | FastAPI + Uvicorn | REST API |
| Frontend | Streamlit | Chat UI |
| Evaluation | RAGAS | Faithfulness & Relevancy metrics |
| Chunking | SemanticSplitterNodeParser | Topic-boundary splitting |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- ~8 GB RAM (for the 4-bit LLM)

### 1. Clone and Install
```bash
git clone https://github.com/R-Mohith24/ClinRAG-.git
cd ClinRAG
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add Your Data
- Place medical PDF textbooks in `data/raw_pdfs/`
- Download BioMistral-7B GGUF to `models/llm/biomistral-7b-Q4_K_M.gguf`

### 3. Build the Index
```bash
python -m src.ingestion.build_index
```

### 4. Start the Application
**Terminal 1 — Backend:**
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend:**
```bash
streamlit run src/ui/app.py
```

Open `http://localhost:8501` in your browser and start asking medical questions!

### 5. Run Evaluation (Optional)
```bash
python -m src.eval.generate_dataset
python -m src.eval.run_ragas
```

---

## 📄 License

This project is developed as an academic IEEE research project. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**R. Mohith** — B.Tech CSE, SRM Institute of Science and Technology
