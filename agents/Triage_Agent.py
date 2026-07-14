from langchain_ollama import ChatOllama  # Swapped from langchain_openai
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState  


llm = ChatOllama(model="qwen2.5:3b")


def triage_agent(state: GraphState) -> GraphState:

    alerts = state['alerts']

    system_prompt = SystemMessage(content="""You are a SOC triage analyst reviewing a sequence of security alerts from a Wazuh monitoring system.
    Your only task: 
    decide whether this alert sequence requires mitigation action.
    Consider the sequence and pattern of events, not just individual alerts in isolation.
    Base your decision only on the alert data provided below. Do not assume information that isn't present.
    Output format: {"mitigation_required": true or false, "reasoning": "one sentence explanation that names the actual events_id or rule_id values from the alert data above that support the decision"}
    """)
    
    human_prompt = HumanMessage(content=str(alerts)) 

    response = llm.invoke([system_prompt, human_prompt])
    # print(response.content) 

    return GraphState(
        session_id=state['session_id'],
        alerts=state['alerts'],
        triage_output={"raw_response": response.content}
        )
        
