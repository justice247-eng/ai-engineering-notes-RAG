type RetrievedSource = {
  citation: string;
  source: string;
  document_id: string;
  chunk_index: number;
  distance: number;
};

type QueryResponse = {
  question: string;
  answer: string;
  sources: RetrievedSource[];
  retrieved_passages: Array<{ citation: string; text: string }>;
  generation_enabled: boolean;
};

const apiBaseUrl = (process.env.RAG_API_URL ?? "http://localhost:8000")
  .replace(/\/$/, "");

async function askRag(question: string): Promise<QueryResponse> {
  const response = await fetch(`${apiBaseUrl}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, top_k: 4 })
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(`RAG API returned ${response.status}: ${message}`);
  }

  return (await response.json()) as QueryResponse;
}

async function main(): Promise<void> {
  const question = process.argv.slice(2).join(" ").trim();

  if (!question) {
    console.error(
      'Usage: npx tsx rag-api-client.ts "What is retrieval-augmented generation?"'
    );
    process.exitCode = 1;
    return;
  }

  const result = await askRag(question);

  console.log("\nAnswer:\n");
  console.log(result.answer);
  console.log("\nSources:");
  for (const source of result.sources) {
    console.log(
      `${source.citation} ${source.source} (chunk ${source.chunk_index})`
    );
  }

  if (!result.generation_enabled) {
    console.log(
      "\nNote: the API returned retrieved evidence only; no LLM endpoint is configured."
    );
  }
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
});
