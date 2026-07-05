import chromadb
import json
# from tools.cloud_trail_filter import normalize_event

# file = open("Temp_Events/cloudtrail_synthetic_pe_dataset.json", "r")
# data = json.load(file)
# file.close()

file = open("ait_data/processed/fox_matched_alerts.json", "r")
data = json.load(file)
file.close()

client = chromadb.PersistentClient(path="./chroma_data")

# adding just one collection for now for fox, but we can add more later if needed 
collection = client.get_or_create_collection(name="wazuh_alerts")

def store_wazuh_alert(alert):
    alert_text = alert["full_log"]

    collection.add(
        documents=[alert_text],
        metadatas=[{
            "scenario": "fox",
            "attack_label": alert["attack_label"],
            "rule_id": alert["rule_id"],
            "rule_level": alert["rule_level"],
            "description": alert["description"],
            "agent_name": alert["agent_name"],
            "agent_id": alert["agent_id"],
            "timestamp": alert["timestamp"]
        }],
        ids=[alert["event_id"]]
    )

for alert in data:
    store_wazuh_alert(alert)

# print ("Total alerts stored in ChromaDB:", len(data))
# print ("alerts:", data)


# for event in data["Records"]:
#     result = normalize_event(event)
#     store_event(result)

# results = collection.get()
# print(results)

results = collection.query(
    query_texts=["sudo root access"],
    n_results=3
)
print(results)