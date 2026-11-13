from state import AgentState
from tools import find_today_post, generate_mcqs, validate_mcqs, save_generated_mcqs

def find_post_node(s):
    r=find_today_post(); return {"post":r.get("post"),"post_id":r.get("post",{}).get("id"),"history":s.get("history",[])+["found_post"]}
def generate_node(s):
    r=generate_mcqs(s["post"]["content"],5); return {"mcqs":r.get("mcqs",[]),"retry_count":s.get("retry_count",0)+1,"history":s.get("history",[])+["generated"]}
def validate_node(s): return {"validation":validate_mcqs(s["mcqs"]),"history":s.get("history",[])+["validated"]}
def route_after_validation(s):
    if s["validation"]["valid"]: return "save"
    if s.get("retry_count",0)>=3: return "finish"
    return "generate"
def save_node(s): save_generated_mcqs(s["post_id"],s["mcqs"]); return {"final":"Saved valid MCQs.","history":s.get("history",[])+["saved"]}
def finish_node(s): return {"final":"Retry limit reached.","history":s.get("history",[])+["failed"]}
