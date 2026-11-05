# RAG Hands-on Projects

Build in order. Each project should have setup instructions, architecture, tests, results and lessons learned.

## 1. Search your own notes — beginner
Load five Markdown or text files, split them into chunks, embed and index them, retrieve top-k passages and print source filenames.
**Success:** relevant passages and source metadata are returned.

## 2. PDF question-answering assistant — beginner/intermediate
Extract PDF text, preserve page numbers, retrieve evidence, generate answers and cite pages.
**Success:** every citation points to a real page containing supporting evidence.

## 3. RAG REST API — intermediate
Build document-ingestion and question-answering endpoints with validation, authentication, rate limits and tests.
**Success:** tests cover valid requests, invalid input and unauthorised access.

## 4. Hybrid search and reranking — intermediate
Compare vector search, lexical search and hybrid retrieval using a labelled question/evidence set. Measure recall@k, precision@k, latency and cost.
**Success:** a short report explains which approach works best and why.

## 5. Secure multi-user RAG — advanced
Implement authentication, server-side authorisation, tenant-aware metadata, adversarial cross-tenant tests, deletion and retention.
**Success:** tests prove private documents cannot be retrieved by unauthorised users.

## 6. Agentic RAG — advanced
Let an agent decide when to search, refine a query or call an approved tool. Add tool allowlists, bounded steps, argument validation and human approval for consequential actions.
**Success:** the agent handles multi-step questions without exceeding limits or accessing unauthorised data.

## Project report template
1. Problem and intended users.
2. Data sources and permissions.
3. Architecture diagram.
4. Technology choices and trade-offs.
5. Setup and run instructions.
6. Test questions and expected evidence.
7. Evaluation results.
8. Security risks and mitigations.
9. Known limitations.
10. Next improvements.