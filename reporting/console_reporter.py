from collections.abc import Iterable
from typing import Any


CloudTrailEvent = dict[str, Any]


def print_event_summaries(events: Iterable[CloudTrailEvent]) -> None:
    for event in events:
        print_event_summary(event)


def print_event_summary(event: CloudTrailEvent) -> None:
    print(
        f"{event['EventTime']} | "
        f"{event['EventName']} | "
        f"{event.get('Username', 'unknown')}"
    )
