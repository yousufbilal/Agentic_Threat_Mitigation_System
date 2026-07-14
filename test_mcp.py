from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
import asyncio

async def main():
    client = MultiServerMCPClient({
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
            "transport": "stdio",
        }
    })
    tools = await client.get_tools()

    llm = ChatOllama(model="qwen2.5:3b")
    agent = create_react_agent(llm, tools)

    response = await agent.ainvoke({"messages": "List the files in /tmp"})
    print(response["messages"][-1].content)

asyncio.run(main())