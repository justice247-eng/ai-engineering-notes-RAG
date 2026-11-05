# 1. Introduction to Retrieval-Augmented Generation

RAG is a system design that retrieves relevant information from an external knowledge source and supplies it to a language model before it answers.

Think of an open-book exam: the question is the user's request, the library is the knowledge base, retrieval finds useful pages, and generation writes an answer using those pages.

## Why use RAG?
- Private knowledge: answer questions about company policies, course notes or product manuals.
- Fresh information: update indexed documents without retraining the model.
- Evidence: return source references alongside answers.
- Domain context: supply specialised terminology.
- Control: manage which documents are searchable and by whom.

RAG can reduce unsupported answers when retrieval is effective. It cannot guarantee correctness.

## Worked example
A student uploads lecture notes and asks: What are the stages of the tourism product life cycle? The application searches the notes, retrieves the relevant passage, supplies it with the question to the LLM, then returns an explanation with the source page.

## RAG versus a normal chatbot
| Normal LLM chatbot | RAG application |
|---|---|
| Uses conversation and learned model knowledge | Also searches external knowledge |
| May not know private documents | Can search authorised private documents |
| Knowledge can be stale | Can use recently indexed material |
| Sources are not automatic | Can return source references |

## Use cases
University study assistant, customer support knowledge base, internal policy assistant, product documentation search, research assistant and Worldora destination assistant.

## When RAG may not be right
Use database queries or deterministic code for exact calculations. Use a normal LLM for simple tasks needing no external knowledge. Consider fine-tuning when the goal is to change model behaviour rather than provide changing facts.

## Knowledge check
1. What does retrieval do?
2. What does generation do?
3. Why might a university use RAG?
4. Does RAG guarantee correctness?

**Key idea:** RAG connects a language model to selected external knowledge at answer time.