from graph import graph

result = graph.invoke({
    "topic": "Python decorators",
    "question": "",
    "answer": "",
    "evaluation": "",
    "explanation": "",
    "next_agent": "",
    "final_response": "",
})

print("\n==============================")
print("FINAL RESPONSE")
print("==============================\n")
print(result["final_response"])
