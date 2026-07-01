import boto3
from dotenv import load_dotenv
import json

load_dotenv()

def get_security_events():
    client = boto3.client('cloudtrail')
    response = client.lookup_events(MaxResults=50)

    for event in response['Events']:
        raw_string = event.get("CloudTrailEvent", "{}")
        unpacked_json = json.loads(raw_string)
        print(unpacked_json)


if __name__ == "__main__":
    events = get_security_events()
