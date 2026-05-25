import boto3
from dotenv import load_dotenv

load_dotenv()

def get_security_events():
    client = boto3.client('cloudtrail')
    response = client.lookup_events(MaxResults=5)

    for event in response['Events']:
        print(event['EventTime'])
        print(event['EventName'])
        print(event['EventSource'])
        print(event.get('Username', 'N/A'))
        print(event.get('SourceIPAddress', 'N/A'))
        print(event.get('ErrorCode', 'None'))
        print(event.get('RequestParameters', {}))