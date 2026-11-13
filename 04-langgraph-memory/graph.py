from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import find_post_node, generate_node, validate_node, save_node, finish_node, route_after_validation

def build_graph(checkpointer):
    g=StateGraph(AgentState)
    for n,f in [("find_post",find_post_node),("generate",generate_node),("validate",validate_node),
                ("save",save_node),("finish",finish_node)]:
        g.add_node(n,f)
        
    g.add_edge(START,"find_post")
    g.add_edge("find_post","generate")
    g.add_edge("generate","validate")
    g.add_conditional_edges("validate",route_after_validation,{"generate":"generate","save":"save","finish":"finish"})
    g.add_edge("save",END)
    g.add_edge("finish",END)
    return g.compile(checkpointer=checkpointer)
