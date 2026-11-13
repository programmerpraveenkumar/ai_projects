from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.tools import tool
model = ChatOllama(model="qwen3:4b", temperature=0)

@tool
def list_students():
    """list the students in the db"""
    print("list the students")
    return ["Arun", "Priya", "Rahul"]
@tool
def insert_student(name: str) -> str:
    """Insert a new student with the given name."""
    print(f"Inserting student: {name}")
    return f"Student {name} inserted successfully."
@tool
def update_student(id:int,name:str):
    """update students in the db by id"""
    print(f"update_student {id} {name}")
    return f"Student {id} {name} updated successfully."
@tool
def delete_student(id:int):
    """delete the students in the db by id """
    print(f"delete the student {id}")
    return f"Student {id}  deleted successfully."



agent = create_agent(
    model=model,
    tools=[list_students,insert_student,update_student,delete_student],
    system_prompt="You are a database assistant."
)

# prompt = "list the students"
# prompt = "insert the student name is arun"
# prompt = "update the student name is kumar and id is 1"
prompt = "delete the student roll no  is 1"

result = agent.invoke({
    "messages": [
        {"role": "user", "content": prompt}
    ]
})
print(result['messages'][-1].content)