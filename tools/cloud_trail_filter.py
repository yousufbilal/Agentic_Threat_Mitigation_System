import json

file = open("Temp_Events/cloudtrail_synthetic_pe_dataset.json", "r")
data = json.load(file)
file.close()

print(data)

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
    print(filtered_event)


normalize_event(data)