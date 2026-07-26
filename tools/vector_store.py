import chromadb
import json
import glob

client = chromadb.PersistentClient(path="./chroma_data/chroma_mitre_mitigation")
collection = client.get_or_create_collection(name="get_mitigation")

def store_mitre_mitigation(mitigation):
    mitigation_text = mitigation["description"]

    collection.add(
        documents=[mitigation_text],
        metadatas=[{"name": mitigation["name"]}],
        ids=[mitigation["id"]]
    )

with open("mitre_mitigations/mitre_mitigations.json","r") as file:
    data = json.load(file)

for mitigation in data["mitigations"]:
    store_mitre_mitigation(mitigation)

print(collection.count())

# # accessing all the json files
# processed_files = glob.glob("ait_data/processed/*_matched_alerts.json")

# for filepath in processed_files:
#     scenario = filepath.split("/")[-1].replace("_matched_alerts.json", "")

#     with open(filepath, "r") as file:
#         data = json.load(file)

#     for alert in data:
#         store_wazuh_alert(alert, scenario)