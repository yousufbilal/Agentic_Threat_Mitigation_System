import chromadb
import json
from tools.cloud_trail_filter import normalize_event

file = open("Temp_Events/cloudtrail_synthetic_pe_dataset.json", "r")
data = json.load(file)
file.close()

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="cloudtrail_events")

def store_event(event):
    event_text = event["event_name"] + " by " + event["username"] + " from " + event["source_ip"] + " at " + event["event_time"]

    event_id = event["event_time"] + "-" + event["event_name"] + "-" + event["source_ip"]

    collection.add(
        documents=[event_text],
        metadatas=[{
            "username": event["username"],
            "source_ip": event["source_ip"],
            "event_time": event["event_time"],
            "event_name": event["event_name"]
        }],
        ids=[event_id]
    )

for event in data["Records"]:
    result = normalize_event(event)
    store_event(result)

results = collection.get()
print(results)