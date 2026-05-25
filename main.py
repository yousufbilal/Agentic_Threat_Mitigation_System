from tools.cloudtrail_reader import get_security_events
from tools.mitre_fetch import fetch_mitre_techniques

def run():
    # Retrieve security events from AWS CloudTrail.
    fetch_mitre_techniques()
    # get_security_events()
run()