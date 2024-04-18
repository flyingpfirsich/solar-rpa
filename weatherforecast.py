#api daten holen

#produktion berechnen

#daten in excel anheften

import requests
from datetime import datetime, timedelta

lat = 52.52
lon = 13.4

def fetch_weather_data(date, last_date, lat, lon):
    url = "https://api.brightsky.dev/weather"
    params = {
        "date": date,
        "last_date": last_date,
        "lat": lat,
        "lon": lon
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Fehler beim Abrufen der Wetterdaten. Statuscode: {response.status_code}")
        return None

def berechne_solar_intensität(date, last_date):
    print(f"Aktuelle Zeit: {date} und in einer Stunde: {last_date}")
    response = fetch_weather_data(date,last_date, lat, lon)
    solar_values = [weather_data['solar'] for weather_data in response['weather']]
    return solar_values
