from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

judge_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def action_correct(outputs: dict, reference_outputs: dict) -> dict:

    # exception handling
    if outputs is None:
        return {"key": "action_correct", "score": 0}
    if "action" not in outputs:
        return {"key": "action_correct", "score": 0}

    model_action = outputs["action"]
    expected_action = reference_outputs["action"]

    if model_action == expected_action:
        score = 1
    else:
        score = 0

    return {"key": "action_correct", "score": score}



def target_correct(outputs: dict, reference_outputs: dict) -> dict:
    # exception handling
    if outputs is None:
        return {"key": "target_correct", "score": 0}

    if "affected_asset" not in outputs:
        return {"key": "target_correct", "score": 0}

    model_target = outputs["affected_asset"]
    expected_target = reference_outputs["target"]

    if model_target == expected_target:
        score = 1
    else:
        score = 0

    return {"key": "target_correct", "score": score}



def severity_correct(outputs: dict, reference_outputs: dict) -> dict:
    # exception handling
    if outputs is None:
        return {"key": "severity_correct", "score": 0}

    if "severity" not in outputs:
        return {"key": "severity_correct", "score": 0}

    model_severity = outputs["severity"].lower()
    expected_severity = reference_outputs["severity"].lower()

    if model_severity == expected_severity:
        score = 1
    else:
        score = 0

    return {"key": "severity_correct", "score": score}



def remediation_quality(outputs: dict, reference_outputs: dict) -> dict:
    if outputs is None:
        return {"key": "remediation_quality", "score": 0}

    prompt = f"""You are grading a SOC remediation plan.

    Golden/expected remediation plan:
    {reference_outputs['remediation_plan']}

    Model's remediation plan:
    {outputs['remediation_plan']}

    Score 1 if the model's plan covers the same critical actions as the golden plan (even with different wording).
    Score 0.5 if it covers some but misses key steps.
    Score 0 if it's substantially wrong or missing.

    Respond with only the number: 0, 0.5, or 1."""

    response = judge_llm.invoke(prompt)
    score = float(response.content.strip())

    return {"key": "remediation_quality", "score": score}