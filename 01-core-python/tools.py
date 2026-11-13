import json
from database import get_today_post, save_mcqs
from qwen import generate_with_qwen

def find_today_post():
    post = get_today_post()
    if not post:
        return {"success": False, "message": "No post found for today."}
    post = dict(post)
    if post.get("published_date"):
        post["published_date"] = post["published_date"].isoformat()
    return {"success": True, "post": post}

def generate_mcqs(post_content, count=5):
    try:
        data = json.loads(generate_with_qwen(post_content, count))
        return {"success": True, "mcqs": data.get("mcqs", [])}
    except Exception as e:
        return {"success": False, "message": str(e)}

def validate_mcqs(mcqs):
    errors = []
    if not isinstance(mcqs, list):
        return {"valid": False, "errors": ["MCQs must be a list."]}
    if len(mcqs) != 5:
        errors.append(f"Expected 5 MCQs, received {len(mcqs)}.")
    fields = ["question","option_a","option_b","option_c","option_d","correct_answer"]
    for i, m in enumerate(mcqs):
        if not isinstance(m, dict):
            errors.append(f"MCQ {i+1}: not an object.")
            continue
        for f in fields:
            if not m.get(f):
                errors.append(f"MCQ {i+1}: missing {f}.")
        if m.get("correct_answer") not in ["A","B","C","D"]:
            errors.append(f"MCQ {i+1}: invalid correct_answer.")
    return {"valid": not errors, "errors": errors}

def save_generated_mcqs(post_id, mcqs):
    save_mcqs(post_id, mcqs)
    return {"success": True, "message": f"{len(mcqs)} MCQs saved."}
