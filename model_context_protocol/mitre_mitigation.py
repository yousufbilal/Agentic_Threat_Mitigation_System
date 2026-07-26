from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from model_context_protocol.mcp_client import mcp_client
from pydantic import BaseModel
from typing import Optional
import asyncio
import json

class MitreTechniqueResult(BaseModel):
    mitigation_technique: Optional[str] = None

llm = ChatOllama(model="qwen2.5:3b", temperature=0)
structured_llm = llm.with_structured_output(MitreTechniqueResult)

async def get_mitre_technique_id(demo_technique_id):
   
   tools = await mcp_client.get_tools()

   allowed_tool_names = (
       "get_mitigations",
   )

   tools_by_name = {}

   for tool in tools:
       if tool.name in allowed_tool_names:
           tools_by_name[tool.name] = tool
   
   filtered_tools = list(tools_by_name.values())

#  tool the LLM can use 
   llm_with_tools = llm.bind_tools(filtered_tools)

#  sometimes model get confused in the prompts 
   tool_prompt = HumanMessage(content=f"Identify the MITRE ATT&CK mitigation for this techniqe id {demo_technique_id}")

   tool_decision = await llm_with_tools.ainvoke([tool_prompt])

   if not tool_decision.tool_calls:
       return None

   call = tool_decision.tool_calls[0]
   tool_to_use = tools_by_name[call["name"]]
  
   result = await tool_to_use.ainvoke(call["args"])
   print(result[0])

   return result

# this runs when i run this file so can leave it here for now dont need to change parameters
if __name__ == "__main__":
    demo_technique_id = "T1110"
    result = asyncio.run(get_mitre_technique_id(demo_technique_id))
    parsed = json.loads(result[0]["text"])
    with open("mitre_mitigations/mitre_mitigations.json", "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=4)
