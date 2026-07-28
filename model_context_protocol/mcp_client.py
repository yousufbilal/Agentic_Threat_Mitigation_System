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





# from langchain_mcp_adapters.client import MultiServerMCPClient

# mcp_client = MultiServerMCPClient(
#     {
#         "mitre": {
#             "url": "http://localhost:8000/mcp",
#             "transport": "streamable_http",
#         }
#     }
# )

# mitre-mcp --http --port 8000