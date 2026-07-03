import boto3
from dotenv import load_dotenv
import json

load_dotenv()

def get_security_events():
    client = boto3.client('cloudtrail')
    response = client.lookup_events(MaxResults=50)


    unpacked_events_list = []

    for event in response['Events']:
        raw_string = event.get("CloudTrailEvent", "{}")
        # Unpack the JSON string into a Python dictionary
        unpacked_json = json.loads(raw_string)
        print(unpacked_json)
        
        unpacked_events_list.append(unpacked_json)

    return unpacked_events_list

if __name__ == "__main__":
    events = get_security_events()