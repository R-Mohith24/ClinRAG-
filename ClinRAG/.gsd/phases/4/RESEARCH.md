# Phase 4 Research Insights: Evaluation (RAGAS)

## Objective
Evaluate the ClinRAG system using **50 medical test queries**, comparing the RAG pipeline against a generic No-RAG baseline. Focus on measuring **Hallucinations vs True Mentions** and system **Latency** (REQ-07, REQ-08).

## RAGAS Framework Integration
[RAGAS](https://docs.ragas.io/) (Retrieval Augmented Generation Assessment) is the industry standard for evaluating RAG pipelines without requiring human-in-the-loop for every query.

To use RAGAS effectively, we need a dataset containing:
1. `question`: The user's query.
2. `contexts`: The retrieved textbook passages (from our FAISS index).
3. `answer`: The generated response (from BioMistral).
4. `ground_truth`: The ideal, perfect answer (pre-written for the 50 questions).

### Key Metrics for IEEE Presentation:
1. **Faithfulness (Hallucination Reduction):** Measures if the generated `answer` is factually derived entirely from the `contexts`. A score of 1.0 means zero hallucinations (every claim in the answer is backed by the retrieved text).
2. **Answer Relevance:** Measures if the `answer` actually addresses the `question`, penalizing incomplete or rambling answers.
3. **Context Precision/Recall:** Measures the quality of our E5-Large-V2 + Semantic Chunker retrieval mechanism.

## Evaluation Strategy

Given this runs locally on CPU via `llama_cpp`, evaluating 50 queries across multiple heavy LLM metrics may take significant time. 

### Step 1: Dataset Generation
We need a script to read a JSON/CSV of 50 test questions, pass them through our `CitationQueryEngine`, record the latency (speed), and save the `(question, answer, contexts, ground_truth)` into an Evaluation Dataset JSON.

### Step 2: RAGAS Execution
We feed the resulting Evaluation Dataset into the RAGAS framework. 
*Note: RAGAS typically uses OpenAI models (GPT-4) as the "judge" to grade the answers. Since the user prefers a 100% local, cost-free setup, we have two choices:*
A. Use a stronger API model (like Gemini/OpenAI) just for the evaluation phase as the remote judge.
B. Try to use our local BioMistral as the judge (often inaccurate for complex parsing, but possible).

*Given the IEEE requirements for rigorous academic grading, using an external API strictly as the "Judge" is usually acceptable even for local systems, but we should default to a local evaluator if possible, or at least structure the code so the user can easily plug in an OpenAI API key for grading.*

## Deliverables for Phase 4
1. `src/eval/generate_dataset.py`: Runs 50 queries through ClinRAG, records latency, parses citations into `contexts`, and saves to `data/eval_results.json`.
2. `src/eval/run_ragas.py`: Loads `eval_results.json`, runs RAGAS metrics, and outputs standard CSV/JSON reports for charting in the IEEE paper.
