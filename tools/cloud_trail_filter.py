import json

file = open("Temp_Events/cloudtrail_synthetic_pe_dataset.json", "r")
data = json.load(file)
file.close()

def normalize_event(data):
    filtered_event = {
        "event_time": data["eventTime"],
        "event_name": data["eventName"],
        "event_source": data["eventSource"],
        "username": data["userIdentity"]["userName"],
        "user_type": data["userIdentity"]["type"],
        "source_ip": data["sourceIPAddress"],
        "aws_region": data["awsRegion"],
        "request_parameters": data["requestParameters"]
    }
    print(json.dumps(filtered_event, indent=4))

for event in data["Records"]:
    normalize_event(event)
