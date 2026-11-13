from langchain_openai import ChatOpenAI
from state import AgentState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def supervisor(state: AgentState):
    question = state.get("question", "")
    evaluation = state.get("evaluation", "")
    explanation = state.get("explanation", "")

    if not question:
        return {"next_agent": "question"}

    # If evaluation failed, regenerate the question.
    if evaluation and evaluation.upper().startswith("FAIL"):
        return {"next_agent": "question"}

    if not evaluation:
        return {"next_agent": "evaluator"}

    if not explanation:
        return {"next_agent": "explanation"}

    return {"next_agent": "final"}
