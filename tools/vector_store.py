import chromadb
import json
import glob

client = chromadb.PersistentClient(path="./chroma_data/chroma_mitre_mitigation")

# wipe and recreate: an un-tagged collection silently breaks the
# where={"domain": domain} filter in agentic_rag.py
client.delete_collection(name="get_mitigation")
collection = client.get_or_create_collection(name="get_mitigation")

def store_mitre_mitigation(mitigation, domain):
    mitigation_text = mitigation["description"]

    collection.add(
        documents=[mitigation_text],
        metadatas=[{"name": mitigation["name"], "domain": domain}],
        # namespaced because the same mitigation id can appear in more than one domain file
        ids=[f"{domain}::{mitigation['id']}"]
    )

domain_files = glob.glob("mitre_mitigations/mitre_mitigations_*.json")

for filepath in domain_files:
    filename = filepath.split("/")[-1]
    domain = filename.removeprefix("mitre_mitigations_").removesuffix(".json")

    with open(filepath, "r") as file:
        data = json.load(file)

    for mitigation in data["mitigations"]:
        store_mitre_mitigation(mitigation, domain)

print(collection.count())

# # accessing all the json files
# processed_files = glob.glob("ait_data/processed/*_matched_alerts.json")

# for filepath in processed_files:
#     scenario = filepath.split("/")[-1].replace("_matched_alerts.json", "")

#     with open(filepath, "r") as file:
#         data = json.load(file)

#     for alert in data:
#         store_wazuh_alert(alert, scenario)