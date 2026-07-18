import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_collection(name="wazuh_alerts")

# Will further clean out the data into nice clean string sequence using string
# because it is more token efficient and less noise on the context window
def get_fox_session():
    """
    Connects to ChromaDB, extracts the active security logs, 
    and packages them to perfectly fit the GraphState layout.
    """

    alerts = collection.get()

    flattend_alerts= []

    for item, ID in zip(alerts["metadatas"],alerts["ids"]):
        convert_str = ", ".join(item["groups"])
        item["groups"] = convert_str
        item.update({
            'events_id':ID
        })
        
         # still need to understand it more 
        sorted_item = {key: item[key] for key in sorted(item)}
    
        # 4. Append that single sorted object ONCE per alert
        flattend_alerts.append(sorted_item)

    initial_state = {
        "session_id": "agent_27",
        "alerts":flattend_alerts,
        "triage_output": None,
        }

    return initial_state

