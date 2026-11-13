import asyncio
import json

from ollama import AsyncClient
from mcp import Client


MCP_URL = "https://mcp.stayker.com/mcp"
MODEL = "qwen3:4b"


def mcp_to_ollama_tool(tool):
    """Convert an MCP tool definition to Ollama's tool format."""

    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or tool.name,
            "parameters": tool.input_schema,
        },
    }


def format_tool_result(result):
    """Convert MCP result content into text for Qwen."""

    parts = []

    for item in result.content:
        if hasattr(item, "text"):
            parts.append(item.text)
        else:
            parts.append(str(item))

    if result.is_error:
        return "Tool returned an error: " + "\n".join(parts)

    if not parts and result.structured_content:
        return json.dumps(result.structured_content, default=str)

    return "\n".join(parts)


async def main():
    # Connect to the MCP server
    async with Client(MCP_URL) as mcp_client:

        # Discover tools
        mcp_result = await mcp_client.list_tools()

        # Convert MCP tools to Ollama tools
        ollama_tools = [
            mcp_to_ollama_tool(tool)
            for tool in mcp_result.tools
        ]

        print("Available MCP tools:")
        for tool in ollama_tools:
            print("-", tool["function"]["name"])

        # Get the user's request
        user_request = input("\nWhat would you like to do? ")

        messages = [
            {
                "role": "user",
                "content": user_request,
            }
        ]

        # Qwen may request a tool call, so allow a few rounds
        async with AsyncClient() as ollama_client:

            for _ in range(5):

                response = await ollama_client.chat(
                    model=MODEL,
                    messages=messages,
                    tools=ollama_tools,
                )

                assistant_message = response.message
                messages.append(assistant_message)

                # If Qwen doesn't request a tool, display its answer
                if not assistant_message.tool_calls:
                    print("\nQwen:", assistant_message.content)
                    break

                # Execute each tool selected by Qwen
                for tool_call in assistant_message.tool_calls:

                    tool_name = tool_call.function.name
                    arguments = tool_call.function.arguments

                    # Only allow tools actually advertised by the MCP server
                    allowed_names = {
                        tool["function"]["name"]
                        for tool in ollama_tools
                    }

                    if tool_name not in allowed_names:
                        tool_output = "Error: tool is not available."
                    else:
                        print(f"\nCalling MCP tool: {tool_name}")
                        print("Arguments:", arguments)

                        try:
                            result = await mcp_client.call_tool(
                                tool_name,
                                arguments,
                            )

                            tool_output = format_tool_result(result)

                        except Exception as exc:
                            tool_output = f"Tool execution failed: {exc}"

                    # Send the result back to Qwen
                    messages.append({
                        "role": "tool",
                        "tool_name": tool_name,
                        "content": tool_output,
                    })

            else:
                print("Stopped after 5 tool-calling rounds.")


if __name__ == "__main__":
    asyncio.run(main())