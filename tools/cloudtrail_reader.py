import boto3
import json
from dotenv import load_dotenv

load_dotenv()

TRUSTED_SOURCES = [
    "config.amazonaws.com",
    "cloudtrail.amazonaws.com",
    "health.amazonaws.com",
    "resource-explorer-2.amazonaws.com"
]

HIGH_RISK_APIS = [
    "AssumeRole",
    "GetSecretValue",
    "DeleteTrail",
    "PutBucketPolicy",
    "CreateUser",
    "AttachUserPolicy",
    "DeleteUser",
    "CreateAccessKey",
    "PutUserPolicy",
    "AddUserToGroup"
]

def is_suspicious(event):
    source_ip = event.get("sourceIPAddress", "")
    event_name = event.get("eventName", "")

    if source_ip in TRUSTED_SOURCES:
        return False

    if event_name in HIGH_RISK_APIS:
        print(f"Suspicious event detected: {event_name} from {source_ip}")
        return True

    return False

def get_security_events():
    client = boto3.client('cloudtrail')
    response = client.lookup_events(MaxResults=50)

    events = []

    for event in response['Events']:
        raw = json.loads(event['CloudTrailEvent'])

        source_ip = raw.get('sourceIPAddress', 'N/A')
        event_name = event['EventName']

        if is_suspicious({"sourceIPAddress": source_ip, "eventName": event_name}):
            events.append({
                "event_time": str(event['EventTime']),
                "event_name": event_name,
                "event_source": event['EventSource'],
                "username": event.get('Username', 'N/A'),
                "source_ip": source_ip,
                "error_code": raw.get('errorCode', None),
                "request_parameters": raw.get('requestParameters', {})
            })
    return events