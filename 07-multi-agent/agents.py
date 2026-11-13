class ResearchAgent:
    def run(self, posts):
        return {"source_posts": posts}

class GeneratorAgent:
    def run(self, content):
        return {"task": "generate_mcqs", "content": content}

class ValidatorAgent:
    def run(self, mcqs):
        errors=[]
        if not isinstance(mcqs,list) or len(mcqs)!=5:
            errors.append("Expected exactly 5 MCQs.")
        return {"valid":not errors,"errors":errors}

class SupervisorAgent:
    def decide(self, validation, retry_count):
        if validation["valid"]:
            return "save"
        if retry_count < 3:
            return "regenerate"
        return "stop"
