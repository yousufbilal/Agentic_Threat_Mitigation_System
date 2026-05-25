import boto3
from dotenv import load_dotenv

load_dotenv()

def get_security_events():
    client = boto3.client('cloudtrail', region_name='eu-north-1')
    response = client.lookup_events(MaxResults=20)
    return response['Events']