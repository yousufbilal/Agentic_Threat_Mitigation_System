import boto3
from dotenv import load_dotenv

load_dotenv()

client = boto3.client('cloudtrail', region_name='eu-north-1')
response = client.lookup_events(MaxResults=5)

for event in response['Events']:
    print(event['EventName'], event['EventTime'])