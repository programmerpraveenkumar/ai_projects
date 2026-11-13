from langchain_openai import ChatOpenAI
from state import AgentState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def explanation_agent(state: AgentState):
    question = state["question"]

    prompt = f"""
You are an Explanation Agent.

Take this MCQ:

{question}

Provide a short explanation of:
1. The correct answer
2. Why it is correct
3. Why the other options are incorrect
"""

    response = llm.invoke(prompt)
    return {"explanation": response.content}
