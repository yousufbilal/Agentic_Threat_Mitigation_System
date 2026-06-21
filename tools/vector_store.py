import chromadb

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

test_event = {
    "event_name": "CreateUser",
    "username": "svc-reporting",
    "source_ip": "198.51.100.77",
    "event_time": "2026-06-18T14:55:02Z"
}


results = collection.get()
print(results)