# RAG Workflow Illustrations

## Indexing

    Source files
         |
         v
    Extract text -> Clean -> Chunk -> Embed -> Vector index
                                  |
                                  +------> Text and metadata store

## Query answering

    User question -> Authenticate and authorise
                            |
                            v
                      Embed question
                            |
                            v
                        Retrieve
                            |
                            v
                    Optional reranking
                            |
                            v
                    Assemble evidence
                            |
                            v
                     Generate answer
                            |
                            v
                   Validate and cite
                            |
                            v
                 Answer with sources

## Agentic RAG loop

    User task -> Agent plans -> Search approved knowledge
                    ^                    |
                    |                    v
                    +---- Need more evidence? ---- No --> Answer

Agentic systems need strict limits: maximum steps, approved tools, permission checks, timeouts and human approval for high-impact actions.