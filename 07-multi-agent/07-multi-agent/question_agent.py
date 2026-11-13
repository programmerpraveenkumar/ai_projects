from langchain_openai import ChatOpenAI
from state import AgentState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def question_agent(state: AgentState):
    topic = state["topic"]

    prompt = f"""
You are a Question Generation Agent.

Generate one multiple-choice question about:
{topic}

Return:
Question:
...

A:
...

B:
...

C:
...

D:
...
"""

    response = llm.invoke(prompt)
    return {"question": response.content}
