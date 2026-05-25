import boto3
from dotenv import load_dotenv

load_dotenv()

def get_security_events():
    client = boto3.client('cloudtrail')
    response = client.lookup_events()

    for events in response['Events']:
        print(events['EventTime'], events['EventName'])
