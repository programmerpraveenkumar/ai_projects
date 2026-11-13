import asyncio




from mcp import Client

MCP_URL = "https://mcp.stayker.com/mcp"


async def main():

    async with Client(MCP_URL) as client:
        response = await client.call_tool(
            "actual_tool_name",
            {
                "argument_name": "argument_value"
            }
        )
        
        print("\n========== TOOL RESPONSE ==========\n")
        print(response)


if __name__ == "__main__":
    asyncio.run(main())