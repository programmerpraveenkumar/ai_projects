# 07 - Multi-Agent LangGraph

A simple multi-agent learning project using LangGraph and LangChain.

## Flow

START
  |
  v
Supervisor
  |
  +--> Question Agent
  |        |
  |        v
  |    Supervisor
  |
  +--> Evaluator Agent
  |        |
  |        v
  |    Supervisor
  |
  +--> Explanation Agent
  |        |
  |        v
  |    Supervisor
  |
  +--> Final Agent
           |
           v
          END

## Agents

- Supervisor: decides which agent should run next.
- Question Agent: generates an MCQ.
- Evaluator Agent: checks the MCQ.
- Explanation Agent: explains the question.
- Final Agent: prepares the final response.

## Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

Mac/Linux:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your OpenAI API key.

Then run:

```bash
python main.py
```

## Learning exercise

After running this version, try changing the supervisor so that:

1. FAIL sends the question back to the Question Agent.
2. PASS sends it to the Explanation Agent.
3. Add a Reviewer Agent.
4. Add retry limits.
5. Add memory/checkpointing.
6. Replace deterministic routing with an LLM supervisor.
