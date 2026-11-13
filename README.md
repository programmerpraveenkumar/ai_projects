# Agentic AI Learning Project

One MCQ-generation project implemented progressively:

1. 01-core-python - Qwen + Python tool-calling agent
2. 02-langchain - LangChain agent
3. 03-langgraph - LangGraph stateful workflow
4. 04-langgraph-memory - LangGraph memory/checkpointing
5. 05-rag-pgvector - PostgreSQL + pgvector RAG foundation
6. 06-evaluation-guardrails - validation/evaluation/guardrails
7. 07-multi-agent - supervisor + specialist agents

All versions use the same basic PostgreSQL data model and Qwen via Ollama.

## Common setup

Install PostgreSQL and Ollama.

Expected Ollama model:

    qwen2.5-coder:7b

If your model name differs, change MODEL in the relevant qwen.py.

Create the database and tables using the schema.sql in each version (or use the common schema below).

Install each version's requirements separately.

Default PostgreSQL configuration:

    host=localhost
    port=5432
    database=agent_db
    user=postgres
    password=postgres

You can override with DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD.

## Learning order

Start with 01 and make sure you understand:

Goal -> Qwen -> tool call -> Python tool -> observation -> Qwen -> next action.

Then compare the same application in LangChain and LangGraph.

This is a learning repository, not a production-ready application.
