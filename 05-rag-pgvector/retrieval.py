def search_similar_posts(conn, embedding, limit=5):
    """Return posts nearest to an embedding using pgvector cosine distance."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, title, content,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM posts
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (embedding, embedding, limit))
        return cur.fetchall()
