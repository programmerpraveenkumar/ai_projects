from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Student Management Server")

# In-memory data for learning
students = [
    {"id": 1, "name": "Arun", "email": "arun@example.com"},
    {"id": 2, "name": "Priya", "email": "priya@example.com"},
    {"id": 3, "name": "Kumar", "email": "kumar@example.com"},
]


@mcp.tool()
def list_students() -> list[dict]:
    """Return all students with their IDs, names, and email addresses."""
    return students


@mcp.tool()
def get_student(student_id: int) -> dict:
    """Get a student by their ID."""
    for student in students:
        if student["id"] == student_id:
            return student

    return {"error": f"Student with ID {student_id} not found"}


@mcp.tool()
def add_student(name: str, email: str) -> dict:
    """Add a new student with a name and email address."""
    if any(s["email"].lower() == email.lower() for s in students):
        return {"error": "A student with this email already exists"}

    new_id = max((s["id"] for s in students), default=0) + 1

    student = {
        "id": new_id,
        "name": name,
        "email": email,
    }

    students.append(student)

    return {
        "message": "Student added successfully",
        "student": student,
    }


if __name__ == "__main__":
    mcp.run()