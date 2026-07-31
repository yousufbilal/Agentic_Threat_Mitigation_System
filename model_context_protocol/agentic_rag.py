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


llm = ChatOllama(model="qwen3:4b", temperature=0)
# llm = ChatOllama(model="qwen2.5:3b", temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
llm_with_tools = llm.bind_tools(([agentic_rag]))

async def run_agent(user_input):
    message = HumanMessage(content=user_input)
    ai_msg = await llm_with_tools.ainvoke([message])

    if not ai_msg.tool_calls:
        return "No tool was called"

    # call the first tool 
    call = ai_msg.tool_calls[0]
    result = await agentic_rag.ainvoke(call["args"])

    return result

if __name__ == "__main__":
    result = asyncio.run(run_agent("T1078 Valid Accounts - adversary uses stolen legitimate credentials to gain unauthorized access"))
    print()
    print("THE RESULT IS ",result)
    print()
