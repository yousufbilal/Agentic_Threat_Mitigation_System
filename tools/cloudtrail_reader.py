import boto3
from dotenv import load_dotenv

load_dotenv()

def get_security_events():

    #connect to AWS CloudTrail
    client = boto3.client('cloudtrail', region_name='eu-north-1')
    
    response = client.lookup_events(
        LookupAttributes=[
            {
                'AttributeKey': 'ReadOnly',
                'AttributeValue': 'false'
            }
        ],
        MaxResults=20
    )
    
    return response['Events']


if __name__ == "__main__":
    events = get_security_events()
    for event in events:
        print(f"Event:  {event['EventName']}")
        print(f"User:   {event.get('Username', 'unknown')}")
        print(f"Time:   {event['EventTime']}")
        print("-" * 40)        