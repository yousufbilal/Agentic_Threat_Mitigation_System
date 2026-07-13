import chromadb
import json

file = open("ait_data/processed/fox_matched_alerts.json", "r")
data = json.load(file)
file.close()

client = chromadb.PersistentClient(path="./chroma_data")

# adding just one collection for now for fox, but we can add more later if needed 
collection = client.get_or_create_collection(name="wazuh_alerts")

# print("Collection created or retrieved:", collection.get(limit=1))  # Print the first document in the collection to verify

def store_wazuh_alert(alert):
    alert_text = alert["full_log"]

    collection.add(
        documents=[alert_text],
        metadatas=[{
            "timestamp": alert["timestamp"],
            # "event_id": alert["event_id"], causing duplication
            "agent_ip": alert["agent_ip"],
            "agent_name": alert["agent_name"],
            "agent_id": alert["agent_id"],
            "rule_id": alert["rule_id"],
            "rule_level": alert["rule_level"],
            "description": alert["description"],
            "groups": alert["groups"],
            # "scenario": "fox",
        }],
        ids=[alert["event_id"]]
    )

for alert in data:
    store_wazuh_alert(alert)
