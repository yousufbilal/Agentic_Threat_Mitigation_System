import boto3
from dotenv import load_dotenv

load_dotenv()

def get_security_events():
    client = boto3.client('cloudtrail')
    response = client.lookup_events(MaxResults=50)

    print("CloudTrail Events:", response['Events'])

    return response['Events']

if __name__ == "__main__":
    events = get_security_events()
    print(events)