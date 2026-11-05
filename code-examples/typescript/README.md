# TypeScript RAG Starter

This folder introduces the TypeScript side of RAG. The first example implements safe, predictable text chunking without any API key. It is a foundation, not a complete semantic retriever.

## Requirements

- Node.js 20 or newer recommended.
- npm.

## Run

    npm init -y
    npm install -D typescript tsx @types/node
    npx tsx chunking.ts

## Call the Python RAG API from TypeScript

Start the Python API using the instructions in `../python/README.md`. In another terminal, install the small TypeScript runner:

```bash
npm init -y
npm install -D typescript tsx @types/node
```

Ask a question:

```bash
npx tsx rag-api-client.ts "What is retrieval-augmented generation?"
```

The client uses Node.js 20's built-in `fetch` and needs no additional HTTP library. If the API is hosted at another address, set `RAG_API_URL` before running it.

## What comes next

A complete TypeScript RAG service typically adds:
1. Document extraction (PDF, HTML, DOCX).
2. An embedding model.
3. A vector or hybrid search database.
4. Retrieval and optional reranking.
5. An LLM generation API.
6. Authentication, authorisation, tests and observability.

Do not use keyword overlap as a substitute for semantic retrieval in production. It is included only to teach the difference between deterministic text processing and embedding-based search.
