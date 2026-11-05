"""Unit tests for the bounded Agentic RAG tool dispatcher."""

import json
from types import SimpleNamespace

from rag_app.agent import AgenticRAG


class FakeStore:
    def search(self, query, top_k=4):
        return [
            {
                "source": "notes.txt",
                "chunk_index": 2,
                "text": f"Evidence for {query}",
            }
        ]

    def list_sources(self):
        return ["notes.txt"]


def make_agent():
    config = SimpleNamespace(
        llm_base_url="",
        llm_api_key="",
        llm_model="",
    )
    return AgenticRAG(config, FakeStore())


def test_agent_search_tool_returns_citation_and_evidence():
    result = make_agent()._call_tool(
        "search_knowledge_base",
        json.dumps({"query": "embeddings", "top_k": 2}),
        citation_prefix="S1",
    )
    assert result["results"][0]["citation"] == "[S1-1]"
    assert result["results"][0]["source"] == "notes.txt"


def test_agent_rejects_unknown_tools():
    result = make_agent()._call_tool("run_shell_command", "{}", "S1")
    assert "error" in result


def test_agent_rejects_invalid_top_k():
    result = make_agent()._call_tool(
        "search_knowledge_base",
        json.dumps({"query": "test", "top_k": 100}),
        citation_prefix="S1",
    )
    assert "error" in result


def test_agent_can_list_sources():
    result = make_agent()._call_tool("list_available_sources", "{}", "S1")
    assert result["sources"] == ["notes.txt"]
