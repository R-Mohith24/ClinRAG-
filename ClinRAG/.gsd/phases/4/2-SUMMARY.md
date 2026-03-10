# Wave 2 Summary – Plan 4.2

**Phase:** 4  
**Plan:** 2 (RAGAS Execution)  
**Status:** ✅ Complete

## What Was Done

### `requirements.txt` / Dependencies
- Installed `ragas`, `datasets`, and `matplotlib`.

### `src/eval/run_ragas.py`
- Created the core evaluation script.
- Loads `data/eval_results.json` into a HuggingFace Dataset.
- **Offline Judge**: Constructed LlamaIndex wrappers (`LlamaIndexLLMWrapper`, `LlamaIndexEmbeddingsWrapper`) so BioMistral and E5-Large evaluate the metrics locally without needing an OpenAI key.
- Measures `faithfulness` (Hallucinations) and `answer_relevancy`.
- Outputs results strictly to `data/ragas_report.csv` for IEEE charting.
