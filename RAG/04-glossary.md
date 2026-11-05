# 4. Core Concepts and Glossary

- **LLM:** a large language model that processes and generates language.
- **Token:** a unit of text processed by a model; not exactly the same as a word.
- **Chunk:** a passage of a document stored and retrieved as one unit.
- **Embedding:** a numerical vector representing semantic features of text.
- **Vector:** an ordered list of numbers.
- **Vector database:** a store that supports similarity search over vectors, often with metadata.
- **Similarity search:** finds vectors close to a query vector under a chosen metric.
- **Retriever:** searches the index and returns candidate passages.
- **Reranker:** reorders candidates by relevance to a question.
- **Metadata:** structured information such as source, page, date, language or owner.
- **Context window:** the maximum input and output tokens a model can process.
- **Prompt:** instructions and content supplied to the model.
- **Grounding:** connecting an answer to supplied evidence and traceable sources.
- **Hallucination:** an unsupported or fabricated model output.
- **Hybrid search:** combines lexical keyword matching and semantic vector search.
- **Top-k:** number of candidates requested from retrieval.
- **Recall:** proportion of all relevant passages that retrieval finds.
- **Precision:** proportion of retrieved passages that are relevant.
- **Citation:** reference connecting a claim to its supporting source.
- **Agentic RAG:** a design where an agent can decide when to retrieve, refine searches or call approved tools.
- **Fine-tuning:** additional model training to change behaviour or task performance; not a substitute for current factual retrieval.

## Check yourself
Explain the difference between an embedding, a chunk, a retriever and a reranker without reading the definitions.