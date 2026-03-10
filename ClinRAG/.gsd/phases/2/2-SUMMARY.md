# Wave 2 Summary – Plan 2.2

**Phase:** 2  
**Plan:** 2 (Chat Engine – CRC with Memory)  
**Status:** ✅ Complete

## What Was Done

### `src/rag/chat_engine.py`
- Created `build_chat_engine(query_engine)` wrapping the CitationQueryEngine in a `CondenseQuestionChatEngine`.
- Added `ChatMemoryBuffer` with `token_limit=1500`.
- `verbose=True` so the condensed query is printed to the console during demos.

### `src/ingestion/chunker.py` (upgraded)
- Replaced naive `SentenceSplitter` (fixed 512-token chunks) with `SemanticSplitterNodeParser`.
- Uses E5-Large-V2 embeddings to detect topic-shift breakpoints dynamically.
- Result: chunks are bounded by medical concept boundaries, not token counts.

## Verification
```
chat_engine.py: OK
chunker.py: OK
--- ALL IMPORTS PASSED ---
```
