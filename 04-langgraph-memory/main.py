from graph import build_graph
from langgraph.checkpoint.memory import InMemorySaver

if __name__ == "__main__":
    checkpointer = InMemorySaver()
    app = build_graph(checkpointer)
    config = {"configurable": {"thread_id": "mcq-learning-demo"}}
    goal = input("What do you want the agent to do? ")
    result = app.invoke({"goal": goal, "post": None, "mcqs": [], "validation": None, "post_id": None, "retry_count": 0, "history": []}, config)
    print(result.get("final"))
