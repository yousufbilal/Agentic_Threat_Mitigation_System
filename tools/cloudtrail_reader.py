import boto3
import json
from dotenv import load_dotenv
from Temp_Events.Events import events
from cloud_trail_filter import is_suspicious

load_dotenv()



# def get_security_events():
#     client = boto3.client('cloudtrail')
#     response = client.lookup_events(MaxResults=50)

#     events = []

#     for event in response['Events']:
#         raw = json.loads(event['CloudTrailEvent'])

#         source_ip = raw.get('sourceIPAddress', 'N/A')
#         event_name = event['EventName']

#         if is_suspicious({"sourceIPAddress": source_ip, "eventName": event_name}):
#             events.append({
#                 "event_time": str(event['EventTime']),
#                 "event_name": event_name,
#                 "event_source": event['EventSource'],
#                 "username": event.get('Username', 'N/A'),
#                 "source_ip": source_ip,
#                 "error_code": raw.get('errorCode', None),
#                 "request_parameters": raw.get('requestParameters', {})
#             })
#     return events