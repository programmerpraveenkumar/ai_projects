from agent import build_agent

if __name__ == "__main__":
    agent = build_agent()
    goal = input("What do you want the agent to do? ")
    result = agent.invoke({"messages": [("user", goal)]})
    print(result["messages"][-1].content)
