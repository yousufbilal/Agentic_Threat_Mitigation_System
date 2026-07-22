import json

def get_session(scenario):
    with open(f"ait_data/processed/{scenario}_matched_alerts.json", "r") as file:
        alerts = json.load(file)

    alert_log_sequence = []

    for alert in alerts:
        alert["groups"] = ", ".join(alert["groups"])
        alert_log_sequence.append(alert["full_log"])
        

    initial_state = {
        "session_id": scenario,
        "alerts": alerts,
        "triage_output": None,
        "alert_log_sequence":alert_log_sequence
    }

    return initial_state


if __name__ == "__main__":
    # Test with a scenario name, e.g., "fox"
    get_session("fox")