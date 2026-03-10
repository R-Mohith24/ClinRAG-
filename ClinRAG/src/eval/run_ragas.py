"""
RAGAS Evaluator
Loads the generated eval_results.json and calculates Faithfulness and Answer Relevancy
using standard local RAGAS metrics, bypassing OpenAI API requirements.
"""

import json
import os
import pandas as pd
from datasets import Dataset

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

# For local evaluation using LlamaIndex wrappers
from ragas.llms import LlamaIndexLLMWrapper
from ragas.embeddings import LlamaIndexEmbeddingsWrapper

from src.llm.biomistral import get_llm
from src.ingestion.embedder import get_embedder

def main():
    print("=" * 60)
    print("ClinRAG - Running RAGAS Evaluation (Local)")
    print("=" * 60)

    input_file = "data/eval_results.json"
    output_file = "data/ragas_report.csv"
    
    if not os.path.exists(input_file):
         print(f"[ERROR] {input_file} not found. Please run generate_dataset.py first.")
         return

    # 1. Load Data
    print(f"[INFO] Loading dataset from {input_file}")
    with open(input_file, "r") as f:
        data = json.load(f)

    # Format for RAGAS
    ragas_dict = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": []
    }
    
    for item in data:
        ragas_dict["question"].append(item["question"])
        ragas_dict["answer"].append(item["answer"])
        ragas_dict["contexts"].append(item["contexts"])
        ragas_dict["ground_truth"].append(item["ground_truth"])
        
    evaluation_dataset = Dataset.from_dict(ragas_dict)
    print(f"[INFO] Dataset loaded with {len(evaluation_dataset)} samples.")

    # 2. Setup Local RAGAS Evaluators (Bypass OpenAI)
    print("[INFO] Initializing local BioMistral-7B as RAGAS Judge...")
    try:
        local_llm = get_llm()
        local_embedder = get_embedder()
        
        # Wrap LlamaIndex models for RAGAS
        ragas_llm = LlamaIndexLLMWrapper(local_llm)
        ragas_embedder = LlamaIndexEmbeddingsWrapper(local_embedder)
        
    except Exception as e:
        print(f"[ERROR] Failed to initialize local evaluator models: {e}")
        print("[INFO] If you want to use OpenAI instead, set your OPENAI_API_KEY environment variable.")
        return

    # 3. Run Evaluation
    print("\n[INFO] Starting Evaluation (This may take significant time on CPU...)")
    metrics = [
        faithfulness,
        answer_relevancy
    ]
    
    try:
        # We pass our local models so RAGAS doesn't try to call OpenAI
        result = evaluate(
            dataset=evaluation_dataset,
            metrics=metrics,
            llm=ragas_llm,
            embeddings=ragas_embedder,
            raise_exceptions=False
        )
    except Exception as e:
        print(f"[ERROR] Evaluation failed: {e}")
        return

    # 4. Save and Output Results
    df = result.to_pandas()
    df.to_csv(output_file, index=False)
    
    print("\n" + "=" * 60)
    print("✅ RAGAS Evaluation Complete!")
    print(f"📊 Results saved to: {output_file}")
    print("\n--- Final Aggregate Scores ---")
    print(result)
    print("=" * 60)


if __name__ == "__main__":
    main()
