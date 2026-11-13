import asyncio
import json
import argparse
from mcp import Client

MCP_URL = "https://mcp.stayker.com/mcp"
parser = argparse.ArgumentParser()

parser.add_argument("--name", type=str,required=False)

parser.add_argument("--type", type=str, required=True)
parser.add_argument("--args", type=str, required=False)


async def main():
    args = parser.parse_args()
    tools = []
    async with Client(MCP_URL) as client:

        if args.type == "list":
            result = await client.list_tools()
            for tool in result.tools:
                print("Tool Name:", tool.name)
                tools.append(tool)

        if args.type == "tool_args":
            result = await client.list_tools()
            for tool in result.tools:
                if tool.name == args.name:
                    print(tool.description)
                    print("_"*10)
                    print(json.dumps(tool.input_schema, indent=2))


        if args.type == "tool_call":
            json_args = json.loads( args.args)
            print(json_args)
            response = await client.call_tool(
                args.name,
                json_args
            )
            for item in response.content:
                if item.type == "text":
                    try:
                        data = json.loads(item.text)
                        print(json.dumps(data, indent=2))
                    except json.JSONDecodeError:
                        print(item.text)

            # print("\n========== TOOL RESPONSE ==========\n")
            # print(response)
            # print(json.dumps(response,indent=2))


if __name__ == "__main__":
    asyncio.run(main())