REQUIRED_FIELDS = ["question","option_a","option_b","option_c","option_d","correct_answer"]

def validate_mcq_structure(mcqs):
    errors=[]
    if not isinstance(mcqs,list): return ["MCQs must be a list."]
    if len(mcqs)!=5: errors.append("Exactly 5 MCQs are required.")
    for i,m in enumerate(mcqs):
        if not isinstance(m,dict):
            errors.append(f"MCQ {i+1} must be an object."); continue
        for f in REQUIRED_FIELDS:
            if not m.get(f): errors.append(f"MCQ {i+1} missing {f}.")
        if m.get("correct_answer") not in ["A","B","C","D"]:
            errors.append(f"MCQ {i+1} has invalid answer.")
    return errors

def apply_guardrails(mcqs):
    errors=validate_mcq_structure(mcqs)
    return {"allowed":not errors,"errors":errors}
