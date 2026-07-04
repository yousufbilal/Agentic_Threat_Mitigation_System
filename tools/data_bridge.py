import json
from itertools import islice

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

for item in ait_data:
    print(item)