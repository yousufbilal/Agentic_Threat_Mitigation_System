import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class CloudTrailConfig:
    region_name: str
    max_results: int
    read_only: str


@dataclass(frozen=True)
class AppConfig:
    cloudtrail: CloudTrailConfig

    @classmethod
    def from_environment(cls) -> "AppConfig":
        load_dotenv()

        return cls(
            cloudtrail=CloudTrailConfig(
                region_name=os.getenv("AWS_REGION", "eu-north-1"),
                max_results=int(os.getenv("CLOUDTRAIL_MAX_RESULTS", "20")),
                read_only=os.getenv("CLOUDTRAIL_READ_ONLY", "false"),
            )
        )
