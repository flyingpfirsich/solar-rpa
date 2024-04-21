import requests
from datetime import datetime, timedelta

def fetch_energy_price():

    now = datetime.now().replace(minute=0).strftime('%Y-%m-%dT%H:%M')

    url = "https://api.energy-charts.info/price"
    params = {
        "bzn": "DE-LU",
        "start": now,
        "end": now
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        price = data.get('price', [None])[0]  # Extrahiere den ersten Preis aus der Liste
        return price
    else:
        print(f"Fehler beim Abrufen der Daten. Statuscode: {response.status_code}")
        return None
    
    