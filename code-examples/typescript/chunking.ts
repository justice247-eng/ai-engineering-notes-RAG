type TextChunk = {
  id: string;
  text: string;
  source: string;
  chunkIndex: number;
};

function chunkText(
  text: string,
  source: string,
  chunkSize = 40,
  overlap = 8
): TextChunk[] {
  if (!Number.isInteger(chunkSize) || !Number.isInteger(overlap)) {
    throw new Error("chunkSize and overlap must be integers");
  }
  if (chunkSize <= 0 || overlap < 0 || overlap >= chunkSize) {
    throw new Error("Require chunkSize > overlap >= 0");
  }

  const words = text.trim().split(/\s+/).filter(Boolean);
  const chunks: TextChunk[] = [];
  let start = 0;

  while (start < words.length) {
    const end = Math.min(start + chunkSize, words.length);
    chunks.push({
      id: `${source}-chunk-${chunks.length}`,
      text: words.slice(start, end).join(" "),
      source,
      chunkIndex: chunks.length
    });

    if (end === words.length) break;
    start = end - overlap;
  }

  return chunks;
}

const notes = [
  {
    source: "tourism-notes.txt",
    text: "Tourism involves travel outside a person's usual environment. Hospitality provides services such as accommodation, food and welcoming guest experiences."
  },
  {
    source: "ai-notes.txt",
    text: "Retrieval augmented generation finds relevant external passages and provides them to a language model as context before it answers."
  }
];

for (const note of notes) {
  const chunks = chunkText(note.text, note.source, 12, 2);
  for (const chunk of chunks) {
    console.log(chunk.id, chunk.text);
  }
}
