"""Command-line interface for the local RAG application."""

import argparse
from pathlib import Path

from .config import settings
from .pipeline import RAGPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingest documents and ask questions with local RAG."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    ingest = commands.add_parser("ingest", help="Index a file or folder")
    ingest.add_argument("path", help="Path to a PDF, TXT, or MD file/folder")

    ask = commands.add_parser("ask", help="Ask a question")
    ask.add_argument("question", help="Question to ask")
    ask.add_argument("--top-k", type=int, default=None)

    commands.add_parser("sources", help="List indexed source filenames")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    pipeline = RAGPipeline(settings)

    if args.command == "ingest":
        path = Path(args.path)
        files = (
            [path]
            if path.is_file()
            else sorted(
                item for item in path.rglob("*")
                if item.is_file() and item.suffix.lower() in {".pdf", ".txt", ".md"}
            )
        )
        if not files:
            raise SystemExit("No supported PDF, TXT, or MD files were found.")
        for file_path in files:
            try:
                result = pipeline.ingest_file(file_path)
                print(
                    f"Indexed {result['source']}: "
                    f"{result['chunks_added']} chunks"
                )
            except (ValueError, OSError) as error:
                print(f"Skipped {file_path}: {error}")

    elif args.command == "ask":
        result = pipeline.ask(args.question, top_k=args.top_k)
        print(f"\nQuestion: {result['question']}\n")
        print(result["answer"])
        for source in result["sources"]:
            print(
                f"{source['citation']} {source['source']} "
                f"(chunk {source['chunk_index']}, "
                f"distance {source['distance']:.4f})"
            )
        for passage in result["retrieved_passages"]:
            print(f"\n{passage['citation']} {passage['text']}")

    elif args.command == "sources":
        for source in pipeline.store.list_sources():
            print(source)


if __name__ == "__main__":
    main()
