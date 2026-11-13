import json
from qwen import ask_qwen
from tools import find_today_post, generate_mcqs, validate_mcqs, save_generated_mcqs

SYSTEM = """You are an MCQ agent.
Goal: create exactly 5 MCQs from today's coding post and save them.
Use tools to find the post, generate MCQs, validate them, and save them.
Never save invalid MCQs. If validation fails, regenerate.
Continue until completed."""

def execute(name, args):
    if name == "find_today_post": return find_today_post()
    if name == "generate_mcqs": return generate_mcqs(args["post_content"], args.get("count",5))
    if name == "validate_mcqs": return validate_mcqs(args["mcqs"])
    if name == "save_mcqs": return save_generated_mcqs(args["post_id"], args["mcqs"])
    return {"success": False, "message": f"Unknown tool: {name}"}

def run_agent(goal):
    messages = [{"role":"system","content":SYSTEM},{"role":"user","content":goal}]
    for i in range(12):
        print(f"\n--- ITERATION {i+1} ---")
        response = ask_qwen(messages)
        msg = response["message"]
        messages.append(msg)
        calls = msg.get("tool_calls", [])
        if calls:
            for call in calls:
                fn = call["function"]
                result = execute(fn["name"], fn.get("arguments", {}))
                messages.append({"role":"tool","content":json.dumps(result, default=str)})
            continue
        content = msg.get("content","").strip()
        try:
            request = json.loads(content)
            if isinstance(request, dict) and "name" in request and "arguments" in request:
                result = execute(request["name"], request["arguments"])
                messages.append({"role":"tool","content":json.dumps(result, default=str)})
                continue
        except json.JSONDecodeError:
            pass
        return content
    return "Maximum iterations reached."
