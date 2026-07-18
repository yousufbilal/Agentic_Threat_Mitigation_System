import chromadb
import json
import glob

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="wazuh_alerts")

def store_wazuh_alert(alert, scenario):
    alert_text = alert["full_log"]

    collection.add(
        documents=[alert_text],
        metadatas=[{
            "timestamp": alert["timestamp"],
            "agent_ip": alert["agent_ip"],
            "agent_name": alert["agent_name"],
            "agent_id": alert["agent_id"],
            "rule_id": alert["rule_id"],
            "rule_level": alert["rule_level"],
            "description": alert["description"],
            "groups": alert["groups"],
            "scenario": scenario,
        }],
        ids=[alert["event_id"]]
    )

# accessing all the json files
processed_files = glob.glob("ait_data/processed/*_matched_alerts.json")

for filepath in processed_files:
    scenario = filepath.split("/")[-1].replace("_matched_alerts.json", "")

    with open(filepath, "r") as file:
        data = json.load(file)

    for alert in data:
        store_wazuh_alert(alert, scenario)

    # print(f"{scenario}: stored {len(data)} alerts")