import requests


def fetch_mitre_techniques():
    # Fetch MITRE ATT&CK techniques from the official repository.
    response = requests.get("https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json")
    data = response.json()

    techniques = []

# Iterate through the objects in the MITRE ATT&CK data and extract techniques.
    for obj in data['objects']:
         if obj['type'] == 'attack-pattern':
             techniques.append(obj)

# Filter techniques relevant to cloud 


    for technique in techniques:
        if 'IaaS' in technique.get('x_mitre_platforms', []):    
            print(technique['name'],technique['description'])
            # print(len(technique['name']))
            return techniques


