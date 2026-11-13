import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:7b"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "find_today_post",
            "description": "Find the latest coding post published today.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_mcqs",
            "description": "Generate exactly five MCQs from coding content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "post_content": {"type": "string"},
                    "count": {"type": "integer"},
                },
                "required": ["post_content", "count"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "validate_mcqs",
            "description": "Validate MCQ structure and answers.",
            "parameters": {
                "type": "object",
                "properties": {"mcqs": {"type": "array"}},
                "required": ["mcqs"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_mcqs",
            "description": "Save valid MCQs into PostgreSQL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer"},
                    "mcqs": {"type": "array"},
                },
                "required": ["post_id", "mcqs"],
            },
        },
    },
]

def ask_qwen(messages):
    r = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "tools": TOOLS, "stream": False},
        timeout=300,
    )
    r.raise_for_status()
    return r.json()

def generate_with_qwen(content, count):
    prompt = f"""Create exactly {count} MCQs from this content.

CONTENT:
{content}

Return JSON only:
{{
  "mcqs": [
    {{
      "question": "...",
      "option_a": "...",
      "option_b": "...",
      "option_c": "...",
      "option_d": "...",
      "correct_answer": "A",
      "explanation": "..."
    }}
  ]
}}
"""
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "format": "json",
        },
        timeout=300,
    )
    r.raise_for_status()
    return r.json()["message"]["content"]
