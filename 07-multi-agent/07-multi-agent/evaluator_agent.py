from langchain_openai import ChatOpenAI
from state import AgentState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def evaluator_agent(state: AgentState):
    question = state["question"]

    prompt = f"""
You are an Evaluation Agent.

Evaluate the following multiple-choice question:

{question}

Check:
1. Is the question clear?
2. Are there exactly 4 options?
3. Is there exactly one correct answer?
4. Are the options reasonable?
5. Is the question technically correct?

Return:
PASS
or
FAIL

If FAIL, explain what needs to be fixed.
"""

    response = llm.invoke(prompt)
    return {"evaluation": response.content}
