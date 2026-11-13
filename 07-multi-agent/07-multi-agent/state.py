from typing import TypedDict

class AgentState(TypedDict):
    topic: str
    question: str
    answer: str
    evaluation: str
    explanation: str
    next_agent: str
    final_response: str
