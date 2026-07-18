import json
import csv
from datetime import datetime, timezone
import os

pe_windows = {}

with open("ait_data/labels/labels.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row["attack"] == "privilege_escalation":
            scenario_name = row["scenario"]
            pe_windows[scenario_name] = {
                "start": float(row["start"]),
                "end": float(row["end"])
            }


def extract_slimmed_alert(alert):
    """Extracts required fields from a raw alert dictionary."""
    return {
        "timestamp": alert.get("@timestamp"),
        "event_id": alert.get("id"),
        "agent_ip": alert.get("agent", {}).get("ip"),
        "agent_name": alert.get("agent", {}).get("name"),
        "agent_id": alert.get("agent", {}).get("id"),
        "rule_id": alert.get("rule", {}).get("id"),
        "rule_level": alert.get("rule", {}).get("level"),
        "description": alert.get("rule", {}).get("description"),
        "groups": alert.get("rule", {}).get("groups"),
        "full_log": alert.get("full_log")
    }


def iso_to_epoch(timestamp_string):
    dt = datetime.strptime(timestamp_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


os.makedirs("ait_data/processed", exist_ok=True)

for scenario, window in pe_windows.items():
    
    matched_alerts = []

    with open(f"ait_data/raw/{scenario}_wazuh.json", "r") as file:
        for line in file:
            if line.strip():
                alert = json.loads(line)
                slimmed_alert = extract_slimmed_alert(alert)

                alert_epoch = iso_to_epoch(slimmed_alert["timestamp"])
                if window["start"] <= alert_epoch <= window["end"]:
                    matched_alerts.append(slimmed_alert)

    print(f"{scenario}: {len(matched_alerts)} matched alerts")

    with open(f"ait_data/processed/{scenario}_matched_alerts.json", "w") as out_file:
        json.dump(matched_alerts, out_file, indent=2)
        