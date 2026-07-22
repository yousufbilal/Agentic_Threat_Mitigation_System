from langchain_mcp_adapters.client import MultiServerMCPClient

mcp_client = MultiServerMCPClient(
    {
        "mitre": {
            "command": "mitre-mcp",
            "args": [],
            "transport": "stdio",
        }
    }
)