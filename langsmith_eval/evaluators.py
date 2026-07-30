def action_correct(outputs: dict, reference_outputs: dict) -> dict:
    return {"key": "action_correct", "score": int(outputs["action"] == reference_outputs["action"])}


def target_correct(outputs: dict, reference_outputs: dict) -> dict:
    return {"key": "target_correct", "score": int(outputs["target"] == reference_outputs["target"])}


def severity_correct(outputs: dict, reference_outputs: dict) -> dict:
    return {"key": "severity_correct", "score": int(outputs["severity"] == reference_outputs["severity"])}