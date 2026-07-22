import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama

async def main():
    print()

    client = MultiServerMCPClient(
        {
            "mitre": {
                "command": "mitre-mcp",
                "args": [],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()

    allowed_tool_names = (
    "get_technique_by_id",
    "get_techniques_by_tactic",
    "get_techniques_used_by_group",
    )

    filtered_tools = []

    for t in tools:
        if t.name in allowed_tool_names:
            filtered_tools.append(t)


    llm = ChatOllama(model="qwen2.5:3b")

    agent = create_react_agent(llm, tools)

    result = await agent.ainvoke(
        {
            "messages": [
                ("user", "What technique is T1078?")
            ]
        }
    )

    for m in result["messages"]:
        print("****************************************")
        print("****************************************")
        print(m)
        print("****************************************")
        print("****************************************")


if __name__ == "__main__":
    asyncio.run(main())