# SPEC.md — Project Specification

> **Status**: `FINALIZED`

## Vision
To build ClinRAG, a "Hallucination-Free" context-aware medical chatbot that uses Retrieval-Augmented Generation (RAG) to provide exact, cited answers directly extracted from verified medical textbooks using a CPU-optimized, production-grade framework.

## Goals
1. Provide highly accurate, user-facing transparent citations (Book, Chapter, Page) for every generated claim.
2. Achieve fast, hardware-accelerated CPU inference (<20s latency) using 4-bit quantized models and llama.cpp.
3. Scientifically validate the system's accuracy and hallucination reduction (>80%) via rigorous evaluations (RAGAS framework and A/B testing).
4. Utilize an optimized production RAG framework (LlamaIndex) for document loading, chunking, and memory handling.

## Non-Goals (Out of Scope)
- Developing custom foundational LLMs or custom embedding models.
- Re-inventing core RAG components like semantic chunking or vector databases from scratch.
- Perfect 100% context preservation (accepting 90-95% as a known state-of-the-art constraint).
- Cloud GPU reliance in the final production deployment (CPU edge deployment is intended). 

## Users
- Medical professionals, students, and researchers evaluating AI hallucination properties who need trusted, verifiable medical text retrieval.

## Constraints
- **Hardware Limitations**: System must run effectively on consumer CPUs (Intel i5/Ryzen 5) with ~16GB RAM.
- **Cost**: Entire software stack must utilize Free and Open-Source tools. 
- **Time/Scope**: 2-Week development deadline requiring targeted usage of LlamaIndex for workflow efficiency.

## Success Criteria
- [ ] RAGAS Faithfulness score > 0.85.
- [ ] System averages < 20s response time on CPU hardware.
- [ ] Grounded Answer Rate > 90% (sentences backed by explicit validation).
- [ ] A/B Testing proves > 80% hallucination reduction vs un-grounded queries.
- [ ] Context Precision > 0.75 and Answer Relevance > 0.80.
- [ ] Zero crashes processing a 50-query batch evaluation.
