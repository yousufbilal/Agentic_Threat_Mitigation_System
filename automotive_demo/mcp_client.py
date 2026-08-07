from langchain_mcp_adapters.client import MultiServerMCPClient

mcp_client = MultiServerMCPClient(
    {
        "chartjs": {
            "command": "npx",
            "args": ["-y", "@ax-crew/chartjs-mcp-server"],
            "transport": "stdio",
        }
    }
)