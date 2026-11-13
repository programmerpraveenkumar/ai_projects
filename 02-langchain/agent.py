from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from tools import find_today_post, generate_mcqs, validate_mcqs, save_mcqs

def build_agent():
    model = ChatOllama(model="qwen2.5-coder:7b", temperature=0)
    tools = [find_today_post, generate_mcqs, validate_mcqs, save_mcqs]
    return create_agent(
        model=model,
        tools=tools,
        system_prompt="""Create exactly 5 MCQs from today's coding post.
Find the post, generate MCQs, validate them, regenerate if invalid, then save valid MCQs."""
    )
