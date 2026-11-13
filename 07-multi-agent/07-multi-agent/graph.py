from langgraph.graph import StateGraph, START, END

from state import AgentState
from supervisor import supervisor
from question_agent import question_agent
from evaluator_agent import evaluator_agent
from explanation_agent import explanation_agent
from final_agent import final_agent

builder = StateGraph(AgentState)

builder.add_node("supervisor", supervisor)
builder.add_node("question", question_agent)
builder.add_node("evaluator", evaluator_agent)
builder.add_node("explanation", explanation_agent)
builder.add_node("final", final_agent)

builder.add_edge(START, "supervisor")

builder.add_conditional_edges(
    "supervisor",
    lambda state: state["next_agent"],
    {
        "question": "question",
        "evaluator": "evaluator",
        "explanation": "explanation",
        "final": "final",
    },
)

builder.add_edge("question", "supervisor")
builder.add_edge("evaluator", "supervisor")
builder.add_edge("explanation", "supervisor")
builder.add_edge("final", END)

graph = builder.compile()
