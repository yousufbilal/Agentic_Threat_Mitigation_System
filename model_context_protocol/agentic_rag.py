from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
import chromadb
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv() 

client = chromadb.PersistentClient(path="./chroma_data/chroma_mitre_mitigation")
collection = client.get_or_create_collection(name="get_mitigation")

@tool
def agentic_rag(query: str) -> str:
    """Search the MITRE mitigation database for a defensive action matching a description of an attack technique."""
    results = collection.query(query_texts=[query], n_results=3)
    documents = results["documents"][0]
    return str(documents)


# llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0)
# llm = ChatOllama(model="qwen3:4b", temperature=0)
llm = ChatOllama(model="qwen2.5:3b", temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
llm_with_tools = llm.bind_tools(([agentic_rag]))

async def run_agent(agent_output,domain): 

    message = HumanMessage(content= f"this is the data you need to find from {agent_output} and the domain is {domain}")
    response = await llm_with_tools.ainvoke([message])

    if not response.tool_calls:
        return "No tool was called"

    for call in response.tool_calls:
        # tool_to_use = call["name"]
        tool_args = call["args"]

    result = await agentic_rag.ainvoke(tool_args)


    return result

