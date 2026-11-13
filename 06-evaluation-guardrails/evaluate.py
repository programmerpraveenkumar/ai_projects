from guardrails import apply_guardrails

def evaluate(mcqs):
    result=apply_guardrails(mcqs)
    return {
        "passed": result["allowed"],
        "score": 1.0 if result["allowed"] else 0.0,
        "errors": result["errors"],
    }

if __name__ == "__main__":
    print(evaluate([]))
