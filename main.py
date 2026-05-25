from tools.cloudtrail_reader import get_security_events

def run():
    events = get_security_events()
    print(events)

run()