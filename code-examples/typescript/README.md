# TypeScript RAG Starter

This folder introduces the TypeScript side of RAG. The first example implements safe, predictable text chunking without any API key. It is a foundation, not a complete semantic retriever.

## Requirements

- Node.js 20 or newer recommended.
- npm.

## Run

    npm init -y
    npm install -D typescript tsx @types/node
    npx tsx chunking.ts

## What comes next

A complete TypeScript RAG service typically adds:
1. Document extraction (PDF, HTML, DOCX).
2. An embedding model.
3. A vector or hybrid search database.
4. Retrieval and optional reranking.
5. An LLM generation API.
6. Authentication, authorisation, tests and observability.

Do not use keyword overlap as a substitute for semantic retrieval in production. It is included only to teach the difference between deterministic text processing and embedding-based search.
