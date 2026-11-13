from state import AgentState
from tools import find_today_post, generate_mcqs, validate_mcqs, save_generated_mcqs

def find_post_node(state: AgentState):
    r=find_today_post()
    return {"post":r.get("post"),"post_id":r.get("post",{}).get("id")}

def generate_node(state: AgentState):
    r=generate_mcqs(state["post"]["content"],5)
    return {"mcqs":r.get("mcqs",[]),"retry_count":state.get("retry_count",0)+1}

def validate_node(state: AgentState):
    return {"validation":validate_mcqs(state["mcqs"])}

def route_after_validation(state):
    if state["validation"]["valid"]:
        return "save"
    if state.get("retry_count",0) >= 3:
        return "finish"
    return "generate"

def save_node(state):
    save_generated_mcqs(state["post_id"],state["mcqs"])
    return {"final":"5 MCQs generated, validated, and saved."}

def finish_node(state):
    return {"final":"Could not produce valid MCQs after the retry limit."}
