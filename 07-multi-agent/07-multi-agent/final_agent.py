from langchain_openai import ChatOpenAI
from state import AgentState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def final_agent(state: AgentState):
    question = state["question"]
    evaluation = state["evaluation"]
    explanation = state["explanation"]

    prompt = f"""
You are the Final Agent.

Prepare the final response for the user.

Question:
{question}

Evaluation:
{evaluation}

Explanation:
{explanation}

Return a clean final MCQ.
"""

    response = llm.invoke(prompt)
    return {"final_response": response.content}
