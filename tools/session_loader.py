import json
import glob
import os

# def get_all_sessions(scenario):
#     """Load every processed attack-category file for a scenario, one session per file."""
#     sessions = []

#     for filepath in sorted(glob.glob(f"ait_data/processed/{scenario}_*_matched_alerts.json")):
#         attack = os.path.basename(filepath)[len(scenario) + 1: -len("_matched_alerts.json")]

#         with open(filepath, "r") as file:
#             alerts = json.load(file)

#         alert_log_sequence = []

#         for alert in alerts:
#             alert["groups"] = ", ".join(alert["groups"])
#             alert_log_sequence.append(alert["full_log"])

#         sessions.append({
#             "session_id": f"{scenario}_{attack}",
#             "alerts": alerts,
#             "triage_output": None,
#             "alert_log_sequence": alert_log_sequence
#         })

#     return sessions


def get_session(scenario):
    with open(f"ait_data/processed/{scenario}_matched_alerts.json", "r") as file:
    # with open(f"poisoned_data/prompt_injection_alerts.json", "r") as file:
    # with open(f"prompt_injected_data_logs/{scenario}_matched_alerts.json", "r") as file:
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