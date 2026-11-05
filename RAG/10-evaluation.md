# RAG Evaluation

A fluent answer does not prove that a RAG system works. Evaluate retrieval and generation separately.

## Build a test set
For realistic questions, label the expected answer, supporting document and passage, whether the answer exists, user permission scope and any conflicting or outdated sources. Keep a held-out test set.

## Retrieval metrics
- Recall@k: fraction of relevant passages found in the top k.
- Precision@k: fraction of top-k results that are relevant.
- Mean reciprocal rank (MRR): rewards finding a relevant result near the top.
- nDCG: evaluates ranking quality when relevance has graded levels.

## Answer metrics
- Faithfulness: are claims supported by retrieved evidence?
- Answer relevance: does the answer address the question?
- Citation correctness: do citations point to supporting passages?
- Completeness: are important parts missing?
- Abstention quality: does the system admit when evidence is insufficient?

LLM-as-judge metrics can help but are not ground truth. Combine them with human review and deterministic checks.

## Operational metrics
Track latency, token usage, provider cost, retrieval errors, ingestion failures, cache hit rate and user feedback. Avoid logging sensitive document content unnecessarily.

## Experiment template
| Run | Chunk strategy | Retriever | top-k | Reranker | Recall@k | Faithfulness | Latency |
|---|---|---|---:|---|---:|---:|---:|
| A | Paragraph | Dense | 5 | No | | | |
| B | Paragraph | Hybrid | 10 | No | | | |
| C | Paragraph | Hybrid | 20 | Yes | | | |

Change one important variable at a time and record the result.

## Run the sample retrieval evaluation

The Python project includes a small labelled dataset at `code-examples/python/evaluation/retrieval_questions.json` and a script at `code-examples/python/evaluate_retrieval.py`.

From `code-examples/python`:

```bash
python -m rag_app.cli ingest sample_docs
python evaluate_retrieval.py
```

The script reports source-level Recall@k, Precision@k and Mean Reciprocal Rank (MRR). These are teaching metrics for a tiny sample set. They do not measure answer faithfulness, citation correctness, latency at scale or production quality. Build a larger, representative, human-labelled test set before comparing real retrievers.
