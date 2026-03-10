---
phase: 4
plan: 2
wave: 2
---

# Plan 4.2: RAGAS Evaluation Execution

## Objective
Build `src/eval/run_ragas.py` to calculate Hallucination and Relevance metrics on the dataset we generated in Plan 4.1.

## Context
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (REQ-07)
- `src/eval/generate_dataset.py` 

## Tasks

<task type="auto">
  <name>Create RAGAS Evaluator Script</name>
  <files>
    - src/eval/run_ragas.py
    - requirements.txt
  </files>
  <action>
    - Add `ragas`, `datasets`, and `matplotlib` to `requirements.txt`.
    - Create `src/eval/run_ragas.py`.
    - The script should:
      - Load `data/eval_results.json` into a HuggingFace `Dataset` object.
      - Import `faithfulness` (Hallucination check) and `answer_relevancy` metrics from `ragas.metrics`.
      - **CRITICAL IEEE REQUIREMENT**: The user is running a 100% local, cost-free setup. RAGAS normally requires an OpenAI key to act as the "Judge". 
      - We will construct a local LLM wrapper using `BioMistral` (or generic `llama-cpp`) to act as the `ragas_llm` and `ragas_embedder` (E5-Large-V2) so the evaluation can run entirely offline without API keys.
      - Run the evaluation.
      - Save the results to `data/ragas_report.csv` for easy import into Excel/IEEE charts.
      - Print the aggregate scores to the console.
  </action>
  <verify>python -m src.eval.run_ragas</verify>
  <done>Script successfully calculates Faithfulness and Answer Relevancy using local models and outputs a CSV report.</done>
</task>

## Success Criteria
- [ ] Requirements updated with `ragas`.
- [ ] Evaluation script built to use local models as the 'Judge'.
- [ ] CSV report successfully generated containing faithfulness and relevance scores.
