from tools.session_loader import get_session
import json

# what get_session gives you
data = get_session("wilson")
print("get_session alert count:", len(data["alerts"]))
print("first alert keys:", data["alerts"][0].keys())

# what's in your golden dataset
with open("golden_dataset_pe.json") as f:
    golden = json.load(f)

golden_alerts = golden["wilson"]["input"]["alerts"]
print("golden dataset alert count:", len(golden_alerts))
print("first alert keys:", golden_alerts[0].keys())