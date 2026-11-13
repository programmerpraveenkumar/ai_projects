from graph import build_graph



if __name__ == "__main__":
    goal = input("What do you want the agent to do? ")
    app = build_graph()
    state = app.invoke({"goal": goal, "post": None, "mcqs": [], "validation": None, "post_id": None, "retry_count": 0})
    print(state.get("final", "Done"))
