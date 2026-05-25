import boto3
from dotenv import load_dotenv

load_dotenv()
# This function retrieves security events from AWS CloudTrail.
def get_security_events():
    client = boto3.client('cloudtrail')
    response = client.lookup_events(MaxResults=5)

    events = []

# Iterate through the events and extract relevant information.
    for event in response['Events']:
     events.append({
            "event_time": str(event['EventTime']),
            "event_name": event['EventName'],
            "event_source": event['EventSource'],
            "username": event.get('Username', 'N/A'),
            "source_ip": event.get('SourceIPAddress', 'N/A'),
            "error_code": event.get('ErrorCode', None),
            "request_parameters": event.get('RequestParameters', {})
        })
     
     return events
