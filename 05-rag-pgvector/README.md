# RAG + pgvector

This phase adds retrieval to the same project.

The key idea is:

User query -> embedding -> pgvector similarity search -> relevant posts -> Qwen -> MCQs.

This is a foundation rather than a dependency-heavy turnkey implementation. You can use pgvector in PostgreSQL and an embedding model available from Ollama or another provider.

Example schema:

CREATE EXTENSION IF NOT EXISTS vector;

ALTER TABLE posts ADD COLUMN IF NOT EXISTS embedding vector(768);

The vector dimension must match the embedding model you choose.

Do not add a vector database merely because you are building an agent. Use retrieval when the problem requires finding relevant information from a larger corpus.
