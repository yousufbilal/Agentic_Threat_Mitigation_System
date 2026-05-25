import requests


def fetch_mitre_techniques():
    # Fetch MITRE ATT&CK techniques from the official repository.
    response = requests.get("https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json")
    print(response.status_code)
    data = response.json()

    techniques = []

# Iterate through the objects in the MITRE ATT&CK data and extract techniques.
    for obj in data['objects']:
         if obj['type'] == 'attack-pattern':
             techniques.append(obj)
            #  print(len(techniques))
             print(techniques[0])
    
    return techniques
