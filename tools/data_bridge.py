import json
import csv
from datetime import datetime, timezone
import os

ait_data = []

with open("ait_data/fox_wazuh.json", "r") as file:
    for line in file:
        if line.strip():
            alert = json.loads(line)

            slimmed_alert = {}
            slimmed_alert["timestamp"] = alert.get("@timestamp")
            slimmed_alert["event_id"] = alert.get("id")
            slimmed_alert["agent_ip"] = alert.get("agent", {}).get("ip")
            slimmed_alert["agent_name"] = alert.get("agent", {}).get("name")
            slimmed_alert["agent_id"] = alert.get("agent", {}).get("id")
            slimmed_alert["rule_id"] = alert.get("rule", {}).get("id")
            slimmed_alert["rule_level"] = alert.get("rule", {}).get("level")
            slimmed_alert["description"] = alert.get("rule", {}).get("description")
            slimmed_alert["groups"] = alert.get("rule", {}).get("groups")
            slimmed_alert["full_log"] = alert.get("full_log")

            ait_data.append(slimmed_alert)

fox_labels = []

with open("ait_data/labels.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row["scenario"] == "fox" and row["attack"] == "privilege_escalation":
            fox_labels.append(row)

start_time = float(fox_labels[0]["start"])
end_time = float(fox_labels[0]["end"])


def iso_to_epoch(timestamp_string):
    dt = datetime.strptime(timestamp_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()

matched_alerts = []

for alert in ait_data:
    alert_epoch = iso_to_epoch(alert["timestamp"])
    if alert_epoch >= start_time and alert_epoch <= end_time:
        matched_copy = dict(alert)
        matched_copy["attack_label"] = "privilege_escalation"
        matched_alerts.append(matched_copy)

print("Total matched alerts:", len(matched_alerts))
print("alerts:",(matched_alerts))

os.makedirs("ait_data/processed", exist_ok=True)

with open("ait_data/processed/fox_matched_alerts.json", "w") as file:
    
    json.dump(matched_alerts, file, indent=2)
