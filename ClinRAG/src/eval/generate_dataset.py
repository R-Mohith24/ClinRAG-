"""
Evaluation Dataset Generator
Loads test_qa.json, runs each question against the local RAG pipeline,
measures latency, and formats outputs for RAGAS evaluation.
"""

import json
import time
import os
from llama_index.core import StorageContext, load_index_from_storage

from src.llm.biomistral import get_llm
from src.rag.query_engine import build_query_engine


def main():
    print("=" * 60)
    print("ClinRAG - Generating RAGAS Evaluation Dataset")
    print("=" * 60)

    # 1. Load pipeline
    print("[INFO] Loading BioMistral LLM and FAISS index...")
    try:
        llm = get_llm()
        storage_context = StorageContext.from_defaults(persist_dir="data/llamaindex_storage")
        index = load_index_from_storage(storage_context)
        query_engine = build_query_engine(index, llm)
    except Exception as e:
        print(f"[ERROR] Failed to load pipeline: {e}")
        return

    # 2. Load questions
    input_file = "data/test_qa.json"
    output_file = "data/eval_results.json"
    
    if not os.path.exists(input_file):
         print(f"[ERROR] Input file {input_file} not found.")
         return

    with open(input_file, "r") as f:
        qa_data = json.load(f)

    print(f"\n[INFO] Loaded {len(qa_data)} questions for evaluation.")
    
    results = []
    
    # 3. Process each question
    for idx, item in enumerate(qa_data, start=1):
        question = item["question"]
        ground_truth = item["ground_truth"]
        
        print(f"\nProcessing [{idx}/{len(qa_data)}]: {question[:50]}...")
        
        # Measure latency
        start_time = time.time()
        response = query_engine.query(question)
        end_time = time.time()
        latency = round(end_time - start_time, 2)
        
        answer = str(response.response)
        
        # Extract explicit context chunks
        contexts = []
        if response.source_nodes:
            for node in response.source_nodes:
                contexts.append(node.node.get_content().strip())
                
        print(f"  -> Generated answer in {latency} seconds.")
        print(f"  -> Retrieved {len(contexts)} citations.")
        
        results.append({
            "question": question,
            "answer": answer,
            "contexts": contexts,
            "ground_truth": ground_truth,
            "latency_seconds": latency
        })

    # 4. Save results
    os.makedirs("data", exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
        
    print("\n" + "=" * 60)
    print(f"✅ Evaluation dataset successfully saved to {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
