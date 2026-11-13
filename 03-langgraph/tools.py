import json
from database import get_today_post, save_mcqs
from qwen import generate_with_qwen

def find_today_post():
    p=get_today_post()
    if not p: return {"success":False}
    p=dict(p)
    if p.get("published_date"): p["published_date"]=p["published_date"].isoformat()
    return {"success":True,"post":p}

def generate_mcqs(content,count=5):
    try: return {"success":True,"mcqs":json.loads(generate_with_qwen(content,count)).get("mcqs",[])}
    except Exception as e: return {"success":False,"mcqs":[],"error":str(e)}

def validate_mcqs(mcqs):
    errors=[]
    if not isinstance(mcqs,list) or len(mcqs)!=5: errors.append("Exactly 5 MCQs required.")
    for i,m in enumerate(mcqs if isinstance(mcqs,list) else []):
        for f in ["question","option_a","option_b","option_c","option_d","correct_answer"]:
            if not m.get(f): errors.append(f"MCQ {i+1}: missing {f}")
        if m.get("correct_answer") not in ["A","B","C","D"]: errors.append(f"MCQ {i+1}: invalid answer")
    return {"valid":not errors,"errors":errors}

def save_generated_mcqs(post_id,mcqs):
    save_mcqs(post_id,mcqs)
