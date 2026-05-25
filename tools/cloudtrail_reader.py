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


  
