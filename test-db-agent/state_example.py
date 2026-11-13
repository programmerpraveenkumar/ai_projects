from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. Define the state structure
class AgentState(TypedDict):
    prompt: str
    operation: str
    result: str


# 2. First node
def understand_request(state: AgentState):
    prompt = state["prompt"].lower()

    if "list" in prompt or "show" in prompt:
        operation = "list"
    elif "insert" in prompt or "add" in prompt:
        operation = "insert"
    else:
        operation = "unknown"

    return {"operation": operation}


# 3. Second node
def prepare_response(state: AgentState):
    operation = state["operation"]

    if operation == "list":
        result = "Ready to list students"
    elif operation == "insert":
        result = "Ready to insert a student"
    else:
        result = "Operation not recognized"

    return {"result": result}


# 4. Build the graph
builder = StateGraph(AgentState)

builder.add_node("understand", understand_request)
builder.add_node("prepare_response", prepare_response)

builder.add_edge(START, "understand")
builder.add_edge("understand", "prepare_response")
builder.add_edge("prepare_response", END)

graph = builder.compile()


# 5. Execute the workflow
result = graph.invoke({
    "prompt": "List all students",
    "operation": "",
    "result": ""
})

print(result)
