import asyncio
import json
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters
from ollama import AsyncClient


MODEL = "qwen3:4b"
SERVER_PATH = Path(__file__).with_name("server.py")


def convert_tool(tool):
    """Convert an MCP tool into Ollama's tool-call format."""
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or tool.name,
            "parameters": tool.input_schema,
        },
    }


def get_result_text(result):
    """Extract text from an MCP tool result."""
    parts = []

    for item in result.content:
        if hasattr(item, "text"):
            parts.append(item.text)

    if result.is_error:
        return "Tool error: " + "\n".join(parts)

    if not parts and result.structured_content is not None:
        return json.dumps(result.structured_content, default=str)

    return "\n".join(parts)


async def main():
    # Launch our local MCP server using the current Python interpreter.
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
    )

    async with Client(server_params) as mcp_client:
        # Discover tools from our own MCP server.
        tool_result = await mcp_client.list_tools()

        ollama_tools = [
            convert_tool(tool)
            for tool in tool_result.tools
        ]

        allowed_tools = {
            tool["function"]["name"]
            for tool in ollama_tools
        }

        print("Available MCP tools:")
        for name in allowed_tools:
            print("-", name)

        async with AsyncClient() as ollama_client:
            while True:
                user_request = input(
                    "\nAsk about students (or type exit): "
                ).strip()

                if user_request.lower() in {"exit", "quit"}:
                    break

                if not user_request:
                    continue

                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a student management assistant. "
                            "Use the provided tools to answer questions "
                            "about students. Call add_student only when "
                            "the user explicitly requests adding a student. "
                            "Do not invent tool results."
                        ),
                    },
                    {
                        "role": "user",
                        "content": user_request,
                    },
                ]

                # Allow multiple tool calls in one request.
                for _ in range(5):
                    response = await ollama_client.chat(
                        model=MODEL,
                        messages=messages,
                        tools=ollama_tools,
                    )

                    assistant_message = response.message
                    messages.append(assistant_message)

                    if not assistant_message.tool_calls:
                        print("\nQwen:", assistant_message.content)
                        break

                    for tool_call in assistant_message.tool_calls:
                        tool_name = tool_call.function.name
                        arguments = tool_call.function.arguments

                        print(f"\nCalling MCP tool: {tool_name}")
                        print("Arguments:", arguments)

                        if tool_name not in allowed_tools:
                            output = "Error: tool is not available."
                        else:
                            try:
                                result = await mcp_client.call_tool(
                                    tool_name,
                                    arguments,
                                )
                                output = get_result_text(result)
                            except Exception as exc:
                                output = f"Tool execution failed: {exc}"

                        print("Tool result:", output)

                        messages.append({
                            "role": "tool",
                            "tool_name": tool_name,
                            "content": output,
                        })
                else:
                    print("Stopped after 5 tool-calling rounds.")


if __name__ == "__main__":
    asyncio.run(main())