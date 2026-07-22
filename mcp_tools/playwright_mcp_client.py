import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama



async def main():
    client = MultiServerMCPClient(
        {
            "playwright": {
                "command": "npx",
                "args": ["@playwright/mcp@latest", "--isolated"],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()

    tools = [t for t in tools if t.name in (
        "browser_navigate",
        "browser_type",
        "browser_press_key",
        "browser_snapshot",
    )]

    llm = ChatOllama(model="qwen2.5:3b")

    agent = create_react_agent(llm, tools)

    result = await agent.ainvoke(
        {
            "messages": [
                (
                    "user",
                    "Navigate to https://en.wikipedia.org, then take a snapshot of the page."
                )
            ]
        }
    )

    for m in result["messages"]:
        print(m)


if __name__ == "__main__":
    asyncio.run(main())