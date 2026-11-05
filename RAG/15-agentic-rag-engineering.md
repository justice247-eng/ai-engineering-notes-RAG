# Agentic RAG Engineering

Agentic RAG adds a decision-making loop around retrieval. Instead of always running one fixed search, an agent can decide which approved retrieval action to take next.

## 1. Basic RAG versus Agentic RAG

**Basic RAG**

```text
Question -> Retrieve -> Generate -> Answer
```

**Agentic RAG**

```text
Question
   |
   v
Agent decides what evidence is needed
   |
   v
Chooses an approved tool
   |
   v
Search / inspect source / refine query
   |
   v
Evaluate whether evidence is sufficient
   |                 |
   | enough          | not enough and budget remains
   v                 v
Generate answer   Another bounded retrieval step
   |
   v
Cited response
```

## 2. Examples of useful tools

A carefully scoped knowledge assistant might expose:

- `search_knowledge_base(query, top_k)`;
- `list_available_sources()`;
- `retrieve_document_section(document_id, section)`;
- `compare_passages(source_a, source_b)`.

Each tool should have a narrow purpose and a validated input schema.

## 3. Bounded execution

An agent must not be allowed to loop forever or call arbitrary functions.

Set explicit limits:

- maximum reasoning/tool steps;
- maximum retrieval results;
- request timeout;
- token and cost budget;
- maximum document size;
- allowed tool list;
- maximum retries.

If the limit is reached, stop and return the evidence gathered so far.

## 4. Authorization comes before retrieval

In a multi-user system, the application must determine which documents the current user may access before searching. Do not rely on the language model to decide whether a user is authorized.

A safe sequence is:

1. Authenticate the caller.
2. Determine tenant and document permissions.
3. Apply server-side metadata filters.
4. Retrieve only authorized chunks.
5. Give the model the filtered evidence.
6. Log the action without exposing private document contents unnecessarily.

## 5. Tool output is untrusted

Documents may contain instructions intended to manipulate the model. Treat retrieved text, tool results and uploaded files as untrusted data. A document must never be able to grant itself permissions or authorize a tool call.

Use allowlisted tools, validate arguments, and require human approval for sensitive or irreversible actions.

## 6. When Agentic RAG is worthwhile

Use it when a question genuinely needs multiple retrieval steps, source comparison, query refinement or a choice among specialized knowledge tools.

Do not add an agent just because it sounds advanced. A simple retrieval pipeline is cheaper, easier to test and often more reliable for straightforward questions.

## 7. Evaluation

Measure more than whether the final answer sounds fluent:

- Did the agent choose the right tool?
- Were tool arguments valid?
- Did it stay within the step and cost budgets?
- Did it retrieve authorized sources only?
- Are the citations correct?
- Did it stop when evidence was insufficient?
