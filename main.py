from config.settings import AppConfig
from reporting.console_reporter import print_event_summaries
from tools.cloudtrail_reader import CloudTrailReader


def run() -> None:
    """Run the threat mitigation workflow."""
    config = AppConfig.from_environment()
    cloudtrail_reader = CloudTrailReader(config.cloudtrail)

    events = cloudtrail_reader.get_security_events()
    print_event_summaries(events)


def main() -> int:
    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
