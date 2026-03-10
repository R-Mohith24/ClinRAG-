---
phase: 4
plan: 1
wave: 1
---

# Plan 4.1: Evaluation Dataset Generation

## Objective
Build `src/eval/generate_dataset.py` to run test queries through our RAG pipeline and measure inference latency.

## Context
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (REQ-07, REQ-08)
- `src/rag/query_engine.py`

## Tasks

<task type="auto">
  <name>Create Evaluation Dataset Generator</name>
  <files>
    - src/eval/generate_dataset.py
    - data/test_qa.json
  </files>
  <action>
    - Create a mock `data/test_qa.json` containing 5 sample medical questions and `ground_truth` answers (as a placeholder for the final 50).
    - Create `src/eval/generate_dataset.py`.
    - Script must initialize the FAISS index and BioMistral LLM.
    - Loop through the test JSON. For each question:
      - Start a timer.
      - Query the `CitationQueryEngine`.
      - Stop timer (record latency in seconds).
      - Extract `response.response` (answer) and `response.source_nodes` (contexts).
    - Save the combined results (question, answer, contexts, ground_truth, latency) to `data/eval_results.json`.
  </action>
  <verify>python -m src.eval.generate_dataset</verify>
  <done>Script successfully outputs a well-formatted eval_results.json containing the required RAGAS fields and latency timings.</done>
</task>

## Success Criteria
- [ ] 5-question placeholder JSON created.
- [ ] Script successfully processes questions through the local BioMistral LLM.
- [ ] Latency is accurately recorded per query.
- [ ] Outputs match the data schema required by RAGAS (`question`, `answer`, `contexts`, `ground_truth`).
