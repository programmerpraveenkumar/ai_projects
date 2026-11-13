from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import find_post_node, generate_node, validate_node, route_after_validation, save_node, finish_node

def build_graph():
    g=StateGraph(AgentState)
    g.add_node("find_post",find_post_node)
    g.add_node("generate",generate_node)
    g.add_node("validate",validate_node)
    g.add_node("save",save_node)
    g.add_node("finish",finish_node)
    g.add_edge(START,"find_post")
    g.add_edge("find_post","generate")
    g.add_edge("generate","validate")
    g.add_conditional_edges("validate",route_after_validation,{"generate":"generate","save":"save","finish":"finish"})
    g.add_edge("save",END)
    g.add_edge("finish",END)
    return g.compile()
