<div align="center">

# Multi Agent Threat Mitigation Framework (MATMF)

![Python](https://img.shields.io/badge/python-3.12-blue)
![LangGraph](https://img.shields.io/badge/orchestration-LangGraph-6E56CF)
![License](https://img.shields.io/badge/license-academic-lightgrey)

</div>

The MATMF is designed as a stateful, non-linear multi-agent orchestration architecture developed to automate triage, forensic investigation, adversarial auditing and remediation planning of security alerts. The agentic system processes Wazuh alerts from the AIT-ADS dataset, focusing on Privilege Escalation scenarios.

## Key Architectural Features

- **Four-agent pipeline** — Triage, Investigator, Adversarial, and Responder agents, each with a distinct, isolated role.
- **Dual-stage Indirect Prompt Injection (IPI) defence** — raw alert data is independently screened by both the Triage and Adversarial Agents before it reaches downstream reasoning.
- **Reject-revise verification loop** — the Adversarial Agent audits the Investigator's findings against raw alert evidence and can send them back for revision, capped at two iterations.
- **MCP-grounded technique attribution** — technique identification is resolved via a live Model Context Protocol connection to a MITRE ATT&CK server, not free-text model inference.
- **Human-in-the-loop execution gate** — every remediation plan pauses for explicit analyst approval before it is persisted; nothing executes automatically.
- **Model-agnostic design** — each agent instantiates its own model client, allowing providers to be swapped without changing the graph topology.

## Quick Start

```bash
git clone https://github.com/yousufbilal/Agentic_Threat_Mitigation_System.git
cd Agentic_Threat_Mitigation_System
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Environment Configuration (.env)

```
GOOGLE_API_KEY=
GROQ_API_KEY=
```

The MITRE MCP server is launched automatically as a stdio subprocess — no separate setup needed.

## Usage

```bash
python main.py                # single scenario, interactive human-approval prompt
python run_all_scenarios.py   # all 8 scenarios, auto-approves human gate
```

## Repository File Structure

```
agents/                  Each agent node (triage, investigator, adversarial, responder, human_approval, prompt_injection_alert)
graph/                   LangGraph state schema and graph builder
model_context_protocol/  MCP client + MITRE technique lookup tool (agentic RAG mitigation-retrieval tool evaluated and removed from the active pipeline — see /legacy)
tools/                   Session loading, alert preprocessing (data_bridge), ingestion, LangSmith upload
ait_data/
  ├── raw/               Raw Wazuh JSON logs (gitignored — not committed)
  ├── labels/            Attack-window labels (start/end timestamps per scenario)
  └── processed/         Alerts sliced to the relevant attack window per scenario
responder_output/        Saved final decisions, one folder per model used
main.py                  Single-scenario interactive run
run_all_scenarios.py     Batch run across all scenarios (auto-approves human gate)
```

## System Architecture & Workflow

<div align="center">
<img width="390" height="435" alt="image" src="https://github.com/user-attachments/assets/e07d35ba-8fa0-49f2-a040-76d240d5eb59" />
</div>

<img width="414" height="630" alt="image" src="https://github.com/user-attachments/assets/75a2e9a2-e4e5-4113-be29-19c40ea3edf2" />

## Dependencies & Tech Stack

**Model Choice.** Gemini 3.7 Flash (gemini-3.7-flash) was chosen as the primary LLM for MATMF because it offers efficient execution and strong support for agent workflows. As the MATMF architecture relies on iterative review loops between agents, connecting to MITRE servers for technique identification via MCP low latency and conditional edges it is vital for the system to be responsive and avoid crashes.

**Runtime.** The MATMF project is implemented in Python version 3.12.13, executed inside a local virtual environment (.venv) rather than the system interpreter; all the dependencies are pinned to the exact version using pip freeze into the requirements.txt file, available in the root for reproducibility. The Agent Orchestration system is built on the LangGraph version (0.6.11) together with LangGraph checkpoint (2.1.2) and prebuilt (0.6.5), layered on top of langchain-core version 1.5.3, with different integration packages installed such as langchain-ollama (0.3.10) for local inference, langchain-groq (1.1.3) for Groq provided models and langchain-google-genai (4.3.2) for Gemini based models, so any agent can be repointed between them. Pydantic version 2.13.4 is used to enforce structured schema validated output. External tools used by the sub-agents are accessed via Model Context Protocol through Langchain-mcp-adapters (0.3.0) together with the Mitre-MCP server (0.3.1). API keys and environment variables are stored in the .env file, loaded via python-dotenv (1.2.1), Langsmith client (0.4.37) allows runs to be recorded, and tracing is available on the LangSmith website.

### Ingestion Bridge and State Initialisation

The Ingestion Bridge processes the raw Wazuh alert data from the AIT-ADS dataset and loads it into the shared GraphState. The bridge also groups alerts based on timestamps across the attack window. This ensures the agents can see the full sequence of events in a Privilege Escalation attack. Keeping only key evidence such as rule IDs, severity levels, host details, timestamps, and raw command logs allows for more streamlined processing by the model at inference.

Once the data is cleaned, the bridge loads it into GraphState by creating the alerts list, the chronological alert_log_sequence, and a unique session_id. It also sets revision_count to 0 and initialises all agent output fields to None.

### Triage Agent

The triage agent is the first agent in the pipeline. It receives AIT-ADS processed alert data which contains the scenario focused on PE threats, reading the normalised alerts list and the alert_log_sequence from GraphState. The triage agent, after receiving the data, must first screen the data for a potential IPI attack if detected divert to the alert prompt injection node. If IPI is not detected it must reason through the alert and produce output. It records its assessment in a structured triage_output object that contains three fields: a mitigation_required boolean flag (True or False), a severity rating (Low, Medium, or High), and a reasoning string that cites specific commands, timestamps, and Wazuh rule IDs. The triage output is then passed to the investigator Agent or discarded if no mitigation is required.

### Investigator Agent

The investigator Agent main task is to review the sequence of security alerts and identify the affected host or account. Investigator achieves this by reasoning over the alerts list, triage_output, and, if present from an earlier loop, the feedback in adversarial_output from GraphState. Before calling the main reasoning model, the Investigator agent sends the processed alert_log_sequence to an external MITRE ATT&CK MCP tool. This tool returns the matching technique_id and technique_name. If the Adversarial Agent rejected an earlier output, the prompt also includes the Adversarial agents feedback so the Investigator can fix the mistake instead of repeating it.

The Investigator agent saves the produced results in a structured investigator_output object. This object holds the affected account, host, IP address, and Wazuh agent ID, along with a list of cited Wazuh rule IDs taken directly from the alert logs. It also includes the technique ID, technique name, MITRE domain, and the reasoning behind the identified entities. Once created, this output is saved to GraphState and passed to the Adversarial Agent for review.

### Adversarial Agent

The Adversarial Agent acts as an independent reviewer that audits the Investigator Agent's findings. It initially reads the raw alerts list, investigator_output, and the current revision_count from GraphState. To prevent IPI attacks from poisoning the pipeline, incoming telemetry is isolated inside strict wrapper tags (<untrusted_alert_data> and <untrusted_investigator_data>). Adversarial Agent performs secondary IPI screening if it detects it, it is diverted to the prompt injection alert node.

If no IPI is detected, proceed with the Investigator Agent's output and do an independent analysis and review to determine whether the affected entity is cited and correct from the alert data or whether the conclusion was wrong check if identified technique is grounded in MITRE ATT&CK and check for a false positive or benign admin activity. The agent produces its result in a structured adversarial_output object containing the verdict ("confirmed" or "rejected"), judgment explanations for the technique and affected entities, and verified rule IDs. If the verdict is rejected, revision_count is incremented by 1, routing the state back to the Investigator Agent for revision; if confirmed, execution transitions downstream to the Responder Agent.

### Reject-Revise Loop

The reject-revise loop exists between the Investigator(actor) and the Adversarial Agent (critic). After the Adversarial Agent completes its review, the state machine evaluates the updated GraphState to choose one of three paths. First, if an IPI is detected, execution immediately routes to the prompt injection alert node, stopping the pipeline to protect downstream components. Secondly, if the findings are rejected and revision_count is two or fewer, the system increments revision_count by 1 and routes the state back to the Investigator Agent for review. Finally, if the findings are confirmed to be correct and contain no IPI or if the revision limit is reached, execution moves forward to the Responder Agent.

<div align="center">
<img width="427" height="144" alt="image" src="https://github.com/user-attachments/assets/4aadf289-6563-423d-a815-0bcf736bb83b" />
<img width="423" height="139" alt="image" src="https://github.com/user-attachments/assets/dc605acb-5b95-4bca-acde-3a241bde6ed9" />
<img width="423" height="236" alt="image" src="https://github.com/user-attachments/assets/a3d7a6e5-8a98-4ca2-b748-6e7fc436f618" />
</div>

### Responder Agent

The Responder Agent is the final agent in the pipeline, responsible for creating the remediation plan for the security analyst. It receives adversarial_output, which includes the affected account, host, IP address, agent ID, technique details, and cited rule IDs, along with the attack domain from investigator_output. Utilising its internal knowledge of the MITRE ATT&CK framework mitigation, it produces the remediation plan. Its agent's results are in a structured responder_output object that defines an action (escalate, contain, or monitor), a severity rating, a confidence score, and explanatory reasoning. It also produces lists of applicable MITRE mitigation names and descriptions, alongside a numbered remediation plan outlining containment steps. Responder Agent's output is then sent downstream to the human_approval.py node.

### System Guardrails and Governance Mechanisms

**Indirect Prompt Injection Implementation.** The framework uses a defence-in-depth principle across two separate checkpoints to protect against IPI attacks. The Triage and Adversarial Agents both ingest raw processed alert data and screen it for IPI attacks. The Investigator Agent also receives the raw alert data between these two checkpoints but does not perform its own independent screening as it relies on Triage's upstream check to filter malicious input before reaching it and Adversarial agent downstream check acts as a secondary safeguard against any payload that evades Triage's screen.

To isolate untrusted data, incoming logs and intermediate outputs are wrapped in boundary tags (<untrusted_alert_data> and <untrusted_investigator_data>) alongside this the models are instructed to treat all internal content purely as data rather than executable directives. If either agent detects an injection attempt, execution immediately diverts to the dedicated prompt_injection_alert node, skipping the remaining downstream agents and the human-approval stage, and alerts the security analyst directly.

**Human-In-The-Loop.** The human-in-the-loop mechanism is present at the human_approval node right after the Responder Agent. Rather than executing the remediation plan, the Responder Agent pauses and presents the remediation plan to the human SOC analyst for review and to get an explicit command to either proceed with the remediation plan by entering "y" and saving it as a JSON file or to enter "n" to discard it.


