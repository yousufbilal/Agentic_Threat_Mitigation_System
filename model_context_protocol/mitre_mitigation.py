from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from model_context_protocol.mcp_client import mcp_client
from pydantic import BaseModel
from typing import Optional
import asyncio
import json
from langchain_google_genai import ChatGoogleGenerativeAI
import chromadb
import json
from dotenv import load_dotenv
load_dotenv() 

# need to implement chromaDB so the new data is taken from the new mitigation


# in this tool we are getting all the mitre mitigation technqiues as the LLM i have is small and its context windoow small so it cant handle the entire data and get the correct mitigation technique for a given attack technique so we are using the agentic_rag tool to get the correct mitigation technique for a given attack technique and then we are using that mitigation technique to get the correct action and remediation plan from the LLM
# this model only provide full list of mitre techniques

class MitreTechniqueResult(BaseModel):
    mitigation_technique: Optional[str] = None

# llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0)
# llm = ChatOllama(model="qwen3:4b", temperature=0)
llm = ChatOllama(model="qwen2.5:3b", temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
structured_llm = llm.with_structured_output(MitreTechniqueResult)

async def get_mitre_mitigation(mitigation_domain):
   
   tools = await mcp_client.get_tools()

   allowed_tool_names = (
       "get_mitigations",
   )

   tools_by_name = {}

   for tool in tools:
       if tool.name in allowed_tool_names:
           tools_by_name[tool.name] = tool
   
   filtered_tools = list(tools_by_name.values())

#    print()
#    print("TOOLS ARE ",filtered_tools)
#    print()

#  tool the LLM can use 
   llm_with_tools = llm.bind_tools(filtered_tools)

#  sometimes model get confused in the prompts 
   tool_prompt = HumanMessage(content=f"Identify the MITRE ATT&CK mitigation for this techniqe id {mitigation_domain}")

   tool_decision = await llm_with_tools.ainvoke([tool_prompt])

   if not tool_decision.tool_calls:
       return None

   for call in tool_decision.tool_calls:
       tool_called = tools_by_name[call["name"]]
       result = await tool_called.ainvoke(call["args"])
       parsed = json.loads(result[0]["text"])
       with open(f"mitre_mitigations/mitre_mitigations_{mitigation_domain}.json", "w", encoding="utf-8") as f:
           json.dump(parsed, f, indent=4)

# this runs when i run this file so can leave it here for now dont need to change parameters
# if __name__ == "__main__":
#     mitigation_domain = "T1110"
#     result = asyncio.run(get_mitre_mitigation(mitigation_domain))
#     parsed = json.loads(result[0]["text"])
#     with open(f"mitre_mitigations/mitre_mitigations{mitigation_domain}.json", "w", encoding="utf-8") as f:
#         json.dump(parsed, f, indent=4)
