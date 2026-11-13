import requests
MODEL="qwen2.5-coder:7b"
def generate_with_qwen(content,count):
    r=requests.post("http://localhost:11434/api/chat",json={"model":MODEL,"messages":[{"role":"user","content":f"Create exactly {count} MCQs from this content. Return JSON only with key mcqs. Each item needs question, option_a, option_b, option_c, option_d, correct_answer, explanation. CONTENT: {content}"}],"stream":False,"format":"json"},timeout=300)
    r.raise_for_status(); return r.json()["message"]["content"]
