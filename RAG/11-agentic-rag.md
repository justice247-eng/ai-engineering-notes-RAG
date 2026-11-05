# Agentic RAG

## What makes RAG agentic?
Basic RAG follows a mostly fixed path: retrieve passages, then generate an answer. In agentic RAG, an agent can choose among approved actions, such as searching another collection, rewriting a query, decomposing a question, retrieving again when evidence is weak, or calling a read-only business tool.

## Example
Question: Compare cancellation rules for two hotels in an itinerary.
1. Identify the hotels.
2. Search the approved policy collection for each.
3. Compare retrieved clauses.
4. Check whether the clauses are current.
5. Return a comparison with citations or disclose missing evidence.

## Basic versus agentic RAG
| Basic RAG | Agentic RAG |
|---|---|
| Mostly fixed retrieval flow | Model chooses among tools and steps |
| Easier to test and control | More flexible but less predictable |
| Usually one retrieval pass | May search and refine repeatedly |
| Lower orchestration complexity | Requires tool governance |

## Guardrails
- Explicit tool allowlist and strict input schemas.
- Maximum steps and tool calls.
- Timeouts, quotas and retry limits.
- Least-privilege credentials.
- Human approval for consequential actions.
- Audit logs and adversarial tests.
- Retrieved documents must never grant new permissions.

Use agentic RAG only when a fixed pipeline is insufficient. More autonomy adds latency, cost and attack surface. Start with ordinary RAG and introduce an agent only when experiments demonstrate a need.