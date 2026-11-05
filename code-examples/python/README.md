# Python Local RAG Starter

This first practical exercise builds a **retrieval-only** pipeline on your computer. It teaches ingestion, chunking, embeddings, vector storage and semantic search before adding an LLM.

## Requirements

- Python 3.10 or newer recommended.
- Internet for the first model download.
- No paid API key is required for this local retrieval exercise.

## Setup

    python -m venv .venv

Activate it:

Windows PowerShell:
    .venv\Scripts\Activate.ps1

macOS/Linux:
    source .venv/bin/activate

Install:

    pip install -r requirements.txt

Run:

    python rag_local.py

## What the program does

1. Defines a few sample knowledge passages.
2. Splits each passage into short chunks.
3. Creates local embeddings with Sentence Transformers.
4. Stores the vectors and text in a persistent Chroma collection.
5. Embeds a question and retrieves the closest passages.
6. Prints each result and its source.

## Files

- rag_local.py — complete retrieval demo.
- requirements.txt — Python dependencies.

## Experiment

Change the question, chunk size, overlap and number of results. Record which passages are retrieved. Try a question whose answer is absent and notice that a vector database still returns the nearest available text; retrieval similarity alone does not prove that evidence answers the question.

## Next step

Add a generation model only after you understand retrieval. Give the model the retrieved passages, require it to say when evidence is insufficient, and display real source metadata. Never hard-code an API key or commit a .env file.
