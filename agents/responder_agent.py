from langchain_ollama import ChatOllama  
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState  

llm = ChatOllama(model="qwen2.5:3b", temperature=0)

def responder_agent(state: GraphState) -> GraphState:

    investigator_output = state["investigator_output"]
    adversarial_output = state["adversarial_output"]

    system_prompt = SystemMessage(content="""You are a SOC responder deciding the mitigation action for a security alert sequence.
    Your only task:
    based on the adversarial reviewer's verdict and the investigator's findings below, decide the mitigation action to take.
    Base your decision only on the data provided below. Do not assume information that isn't present.
    Output format: {"action": "short action label", "target": "affected account/host", "justification": "one sentence explanation referencing the verdict and technique"}
    """)

    human_prompt = HumanMessage(content=str({"investigator_output": investigator_output, "adversarial_output": adversarial_output}))

    response = llm.invoke([system_prompt, human_prompt])
    # print(response.content)

    return GraphState(
        responder_output={"raw_response": response.content}
    )