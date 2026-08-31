from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
import chromadb
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import time
from dotenv import load_dotenv
load_dotenv()

# need to implement chromaDB so the new data is taken from the new mitigation

client = chromadb.PersistentClient(path="./chroma_data/chroma_mitre_mitigation")
collection = client.get_or_create_collection(name="get_mitigation")

@tool
def agentic_rag(query: str, domain: str) -> str:
    """Search the MITRE mitigation database for a defensive action matching a description of an attack technique."""
    results = collection.query(query_texts=[query], n_results=5, where={"domain": domain})
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    return str({"documents": documents, "metadatas": metadatas})


# llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)

# llm = ChatOllama(model="qwen2.5:3b", temperature=0)

# MODEL_NAME = "groq-llama-3.3-70b-versatile"
# llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# MODEL_NAME = "qwen3:4b"
# llm = ChatOllama(model="qwen3:4b", temperature=0)

MODEL_NAME = "gemini-3.7-flash"
llm = ChatGoogleGenerativeAI(model="gemini-3.7-flash", temperature=0)

llm_with_tools = llm.bind_tools(([agentic_rag]))

async def run_agent(agent_output,domain):

    start_time = time.time()

    message = HumanMessage(content= f"this is the data you need to find from {agent_output} and the domain is {domain}")
    response = await llm_with_tools.ainvoke([message])

    if not response.tool_calls:
        end_time = time.time()
        agent_execution_time = end_time - start_time
        print(f"Agentic RAG Sub-Agent Response Time: {agent_execution_time:.2f} seconds")
        return "No tool was called"

    for call in response.tool_calls:
        # tool_to_use = call["name"]
        tool_args ={**call["args"], "domain": domain}

    result = await agentic_rag.ainvoke(tool_args)

    end_time = time.time()
    agent_execution_time = end_time - start_time
    print(f"Agentic RAG Sub-Agent Response Time: {agent_execution_time:.2f} seconds")

    return result

