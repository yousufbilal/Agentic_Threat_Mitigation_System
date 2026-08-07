import webbrowser

import pandas as pd
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
import asyncio
import mcp_client
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv() 

# llm = ChatOllama(model="qwen2.5:3b", temperature=0)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def load_raw_data(csv_path, sample_size=20):
    df = pd.read_csv(csv_path)
    sample = df.sample(n=sample_size, random_state=42)
    return sample.to_csv(index=False)

async def automotive_insight_agent(question, csv_path):
        # need to change name of the server in mcp_client.py to "chartjs" to match this code
        tools = await mcp_client.mcp_client.get_tools()

        generate_chart_tool = next((t for t in tools if t.name == "generateChart"), None)

        # error handling if tool not found
        if generate_chart_tool is None:
            raise ValueError("generateChart tool not found in MCP tools.")

        # given the tool, bind it to the LLM
        llm_with_tools = llm.bind_tools([generate_chart_tool])

        system_message = SystemMessage(content="""You are an AI analyst for Automotive Insights (AIRS), a UK automotive market intelligence platform.

        You will be given:
        1. A user's question about automotive consumer survey data
        2. The raw survey data as CSV rows

        Your job:
        1. Analyze the raw data yourself to answer the question — count, group, and calculate whatever is needed. Show your reasoning briefly if it helps accuracy, but do not include it in the final answer.
        2. Answer in plain English, using only the data provided. Keep it concise (2-3 sentences), written for a business decision-maker.
        3. State the actual figures you calculated from the data — do not estimate or round loosely.
        4. After answering, you MUST call the `generateChart` tool with your findings. This step is mandatory.

        Chart rules:
        - Use "bar" as the chart type unless the question specifically calls for a trend over time (use "line") or a simple proportion of a whole (use "pie" or "doughnut").
        - Only include "scales" (xAxes/yAxes) in the chart options if the type is "bar" or "line". Never include scales for "pie" or "doughnut" charts — they do not use axes.
        - The chart's data values must exactly match the figures you stated in your written answer. Do not introduce new numbers in the chart that weren't in your analysis.
        - Labels must be the exact category names used in the data (e.g. actual age group ranges), not invented groupings.

        Chart Tool Schema Expectations:
        - `chartConfig`: A JSON object matching Chart.js v4 specification.
          Example:
          {
            "type": "bar",
            "data": {
              "labels": ["18-24", "25-34", "35-44"],
              "datasets": [{"label": "EV Interest Count", "data": [5, 12, 3]}]
            },
            "options": {"plugins": {"title": {"display": true, "text": "EV Consideration by Age Group"}}}
          }
        - "outputFormat": "png"
        """)

        raw_data = load_raw_data(csv_path)
        human_message = HumanMessage(content=f"Question: {question}\nRaw survey data (CSV):\n{raw_data}")

        llm_response = await llm_with_tools.ainvoke([system_message, human_message])
        print("Content:", llm_response.content)
        # print("Tool calls:", llm_response.tool_calls)


        if llm_response.tool_calls:
            for call in llm_response.tool_calls:
                print("Calling tool:", call["name"])
                tool_result = await generate_chart_tool.ainvoke(call["args"])

                # html_content = tool_result[0]["text"]
                # with open("chart_output.html", "w") as f:
                #   f.write(html_content)

                # with open("chart.html", "w", encoding="utf-8") as f:
                #   f.write(tool_result)
            
                # webbrowser.open("chart.html")

                print("Tool result:", tool_result)

        return llm_response.content

if __name__ == "__main__":
    asyncio.run(automotive_insight_agent(
        # the agent can create charts of type: bar • line • pie • doughnut • scatter • bubble • radar • polarArea
        question="Which age group is most likely to consider an EV for their next vehicle? make a bar chart showing the proportion of each age group that would consider an EV for their next vehicle.",
        csv_path="automotive_demo/ev_perceptions_synthetic.csv"
    ))