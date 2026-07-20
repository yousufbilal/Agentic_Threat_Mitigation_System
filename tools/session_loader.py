import json

def get_session(scenario):
    with open(f"ait_data/processed/{scenario}_matched_alerts.json", "r") as file:
        alerts = json.load(file)

    for alert in alerts:
        alert["groups"] = ", ".join(alert["groups"])

    initial_state = {
        "session_id": scenario,
        "alerts": alerts,
        "triage_output": None,
    }

    return initial_state