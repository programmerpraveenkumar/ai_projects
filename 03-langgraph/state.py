from typing import TypedDict, Any

class AgentState(TypedDict, total=False):
    goal: str
    post: Any
    post_id: int
    mcqs: list
    validation: dict
    retry_count: int
    final: str
