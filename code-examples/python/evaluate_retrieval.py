"""Evaluate source-level retrieval against a small labelled question set."""

import json
from pathlib import Path

from rag_app.config import settings
from rag_app.pipeline import RAGPipeline


DATASET = Path(__file__).parent / "evaluation" / "retrieval_questions.json"


def reciprocal_rank(hits: list[dict], expected_sources: set[str]) -> float:
    for rank, hit in enumerate(hits, start=1):
        if hit["source"] in expected_sources:
            return 1.0 / rank
    return 0.0


def main(top_k: int = 4) -> None:
    questions = json.loads(DATASET.read_text(encoding="utf-8"))
    pipeline = RAGPipeline(settings)
    recall_scores = []
    precision_scores = []
    reciprocal_ranks = []

    for item in questions:
        expected = set(item["expected_sources"])
        hits = pipeline.store.search(item["question"], top_k=top_k)
        retrieved = {hit["source"] for hit in hits}
        recall = len(expected & retrieved) / len(expected) if expected else 0.0
        precision = (
            len(expected & retrieved) / len(retrieved) if retrieved else 0.0
        )
        mrr = reciprocal_rank(hits, expected)

        recall_scores.append(recall)
        precision_scores.append(precision)
        reciprocal_ranks.append(mrr)

        print(f"Question: {item['question']}")
        print(f"  Expected: {', '.join(sorted(expected))}")
        print(f"  Retrieved: {', '.join(sorted(retrieved)) or '(none)'}")
        print(
            f"  Recall: {recall:.2f} | Precision: {precision:.2f} | "
            f"Reciprocal rank: {mrr:.2f}\n"
        )

    count = len(questions) or 1
    print("Aggregate source-level metrics")
    print(f"  Mean Recall@{top_k}: {sum(recall_scores) / count:.3f}")
    print(f"  Mean Precision@{top_k}: {sum(precision_scores) / count:.3f}")
    print(f"  MRR@{top_k}: {sum(reciprocal_ranks) / count:.3f}")
    print(
        "Note: this small teaching dataset measures source-level retrieval, "
        "not answer faithfulness or production quality."
    )


if __name__ == "__main__":
    main()
