CREATE EXTENSION IF NOT EXISTS vector;

-- Adjust 768 to the dimension of your chosen embedding model.
ALTER TABLE posts ADD COLUMN IF NOT EXISTS embedding vector(768);

CREATE INDEX IF NOT EXISTS posts_embedding_idx
ON posts USING hnsw (embedding vector_cosine_ops);

-- Example semantic search:
-- SELECT id, title, content
-- FROM posts
-- WHERE embedding IS NOT NULL
-- ORDER BY embedding <=> %s
-- LIMIT 5;
