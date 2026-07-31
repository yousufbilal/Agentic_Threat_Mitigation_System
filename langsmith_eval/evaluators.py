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

    model_target = outputs["target"]
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