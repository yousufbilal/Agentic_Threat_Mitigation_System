import boto3
from typing import Any

from config.settings import CloudTrailConfig

CloudTrailEvent = dict[str, Any]


class CloudTrailReader:
    """Adapter for reading security-relevant events from AWS CloudTrail."""

    def __init__(self, config: CloudTrailConfig) -> None:
        self.config = config
        self.client = boto3.client("cloudtrail", region_name=config.region_name)

    def get_security_events(self) -> list[CloudTrailEvent]:
        response = self.client.lookup_events(
            LookupAttributes=[
                {
                    "AttributeKey": "ReadOnly",
                    "AttributeValue": self.config.read_only,
                }
            ],
            MaxResults=self.config.max_results,
        )

        return response["Events"]
