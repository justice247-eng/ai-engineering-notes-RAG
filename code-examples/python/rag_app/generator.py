"""Optional generation through any OpenAI-compatible chat endpoint."""

import httpx

from .config import Settings


class OpenAICompatibleGenerator:
    """Works with local Ollama or compatible hosted endpoints.

    No provider is called unless LLM_BASE_URL and LLM_MODEL are configured.
    Hosted providers may charge for usage; check their current pricing.
    """

    def __init__(self, config: Settings):
        self.base_url = config.llm_base_url
        self.api_key = config.llm_api_key
        self.model = config.llm_model

    @property
    def enabled(self) -> bool:
        return bool(self.base_url and self.model)

    def generate(self, question: str, context: str) -> str | None:
        if not self.enabled:
            return None

        system_message = (
            "You are a careful question-answering assistant. Answer only "
            "from the supplied context. If the context does not contain "
            "enough evidence, say so. Cite supporting passages using their "
            "labels, such as [1] or [2]. Never invent sources."
        )
        user_message = (
            f"QUESTION:\n{question}\n\n"
            f"CONTEXT:\n{context}\n\n"
            "Write a concise answer with citations. If the evidence is "
            "insufficient, clearly state what is missing."
        )
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json={
                "model": self.model,
                "temperature": 0.1,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
            },
            timeout=90.0,
        )
        response.raise_for_status()
        payload = response.json()
        return payload["choices"][0]["message"]["content"].strip()
