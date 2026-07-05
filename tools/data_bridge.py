import json
import csv
from datetime import datetime, timezone

ait_data = []

with open("ait_data/fox_wazuh.json", "r") as file:
    for line in file:
        if line.strip():
            alert = json.loads(line)

            slimmed_alert = {}
            slimmed_alert["timestamp"] = alert.get("@timestamp")
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
        if row["scenario"] == "fox":
            fox_labels.append(row)

def iso_to_epoch(timestamp_string):
    dt = datetime.strptime(timestamp_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()

matched_alerts = []

for alert in ait_data:
    alert_epoch = iso_to_epoch(alert["timestamp"])

    for label in fox_labels:
        start = float(label["start"])
        end = float(label["end"])

        if alert_epoch >= start and alert_epoch <= end:
            alert["attack_label"] = label["attack"]
            matched_alerts.append(alert)

print("Total matched alerts:", len(matched_alerts))
