"""
A/B Test: RAG vs No-RAG (Direct LLM)
Core novel contribution for the IEEE paper.
Proves that the RAG pipeline reduces hallucinations compared to a bare LLM answer.
"""

import json
import time
import os

from llama_index.core import StorageContext, load_index_from_storage

from src.llm.biomistral import get_llm
from src.rag.query_engine import build_query_engine


def get_rag_answer(query_engine, question: str) -> dict:
    """Run question through the full RAG pipeline."""
    start = time.time()
    response = query_engine.query(question)
    latency = round(time.time() - start, 2)
    contexts = [n.node.get_content().strip() for n in response.source_nodes] if response.source_nodes else []
    return {
        "answer": str(response.response),
        "contexts": contexts,
        "latency_seconds": latency,
    }


def get_no_rag_answer(llm, question: str) -> dict:
    """Run question directly through BioMistral with NO retrieval (baseline)."""
    start = time.time()
    response = llm.complete(question)
    latency = round(time.time() - start, 2)
    return {
        "answer": str(response.text),
        "contexts": [],  # No retrieval — no citations
        "latency_seconds": latency,
    }


def main():
    print("=" * 60)
    print("ClinRAG — A/B Test: RAG vs No-RAG Baseline")
    print("=" * 60)

    input_file = "data/test_qa.json"
    output_file = "data/ab_test_results.json"

    if not os.path.exists(input_file):
        print(f"[ERROR] {input_file} not found.")
        return

    with open(input_file, "r") as f:
        qa_data = json.load(f)

    print(f"[INFO] Loaded {len(qa_data)} questions.")

    # Load pipeline
    print("[INFO] Loading BioMistral LLM...")
    llm = get_llm()

    print("[INFO] Loading FAISS index...")
    storage_context = StorageContext.from_defaults(persist_dir="data/llamaindex_storage")
    index = load_index_from_storage(storage_context)
    query_engine = build_query_engine(index, llm)

    results = []

    for idx, item in enumerate(qa_data, start=1):
        question = item["question"]
        ground_truth = item["ground_truth"]
        print(f"\n[{idx}/{len(qa_data)}] {question[:60]}...")

        rag = get_rag_answer(query_engine, question)
        no_rag = get_no_rag_answer(llm, question)

        results.append({
            "question": question,
            "ground_truth": ground_truth,
            "rag": rag,
            "no_rag": no_rag,
        })

        print(f"  RAG latency    : {rag['latency_seconds']}s | citations: {len(rag['contexts'])}")
        print(f"  No-RAG latency : {no_rag['latency_seconds']}s | citations: 0")

    os.makedirs("data", exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    print("\n" + "=" * 60)
    print(f"✅ A/B test results saved to: {output_file}")
    print("Feed this file into run_ragas.py to measure hallucination delta.")
    print("=" * 60)


if __name__ == "__main__":
    main()
