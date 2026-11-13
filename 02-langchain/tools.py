import json
from langchain_core.tools import tool
from database import get_today_post, insert_mcqs
from qwen import generate_with_qwen

@tool
def find_today_post() -> dict:
    """Find the latest coding post published today."""
    post = get_today_post()
    if not post:
        return {"success": False, "message": "No post found."}
    post = dict(post)
    if post.get("published_date"):
        post["published_date"] = post["published_date"].isoformat()
    return {"success": True, "post": post}

@tool
def generate_mcqs(post_content: str, count: int = 5) -> dict:
    """Generate MCQs from coding content."""
    return {"success": True, "mcqs": json.loads(generate_with_qwen(post_content, count)).get("mcqs", [])}

@tool
def validate_mcqs(mcqs: list) -> dict:
    """Validate MCQ structure."""
    errors=[]
    if not isinstance(mcqs,list) or len(mcqs)!=5:
        errors.append("Exactly 5 MCQs are required.")
    fields=["question","option_a","option_b","option_c","option_d","correct_answer"]
    for i,m in enumerate(mcqs if isinstance(mcqs,list) else []):
        for f in fields:
            if not m.get(f): errors.append(f"MCQ {i+1}: missing {f}")
        if m.get("correct_answer") not in ["A","B","C","D"]:
            errors.append(f"MCQ {i+1}: invalid answer")
    return {"valid":not errors,"errors":errors}

@tool
def save_mcqs(post_id: int, mcqs: list) -> dict:
    """Save valid MCQs to PostgreSQL."""
    insert_mcqs(post_id, mcqs)
    return {"success":True,"message":f"{len(mcqs)} MCQs saved."}

