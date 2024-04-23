import requests
import datetime
import pytz

def get_weather_data(solarpark):
    # Extrahiere die Koordinaten aus dem solarpark Dictionary
    lat, lon = solarpark["standort_koordinaten"]

    # Definiere die Zeitzone für Berlin
    timezone = pytz.timezone("Europe/Berlin")

    # Hole das aktuelle Datum und die Uhrzeit in dieser Zeitzone
    now = datetime.datetime.now(timezone)
    
    # Formatiere Datum und Uhrzeit auf das ISO 8601-Format
    date = now.isoformat()

    # URL für den API-Aufruf vorbereiten
    url = f"https://api.brightsky.dev/weather?lat={lat}&lon={lon}&date={date}"

    try:
        # API-Aufruf durchführen3
        response = requests.get(url)
        response.raise_for_status()  # Überprüft, ob die Anfrage erfolgreich war

        # JSON-Daten aus der Antwort extrahieren
        weather_data = response.json()

        # Hier können Sie wählen, welche Daten zurückgegeben oder weiter verarbeitet werden sollen
        return weather_data

    except requests.exceptions.RequestException as e:
        # Fehlerhandling für den Fall, dass die API nicht erreichbar ist oder ein anderer Fehler auftritt
        print(f"An error occurred: {e}")
        return None


def get_price_data(solarpark):
    # Bereite das Datum für vorgestern und heute vor
    today = datetime.date.today()
    twodaysago = today - datetime.timedelta(days=2)

    # Konvertiere die Daten in das benötigte String-Format (YYYY-MM-DD)
    start_date = twodaysago.isoformat()
    end_date = today.isoformat()

    # Setze den Bidding Zone Parameter fest
    bzn = "DE-LU"

    # URL für den API-Aufruf vorbereiten
    url = f"https://api.energy-charts.info/price?bzn={bzn}&start={start_date}&end={end_date}"

    try:
        # API-Aufruf durchführen
        response = requests.get(url)
        response.raise_for_status()  # Überprüft, ob die Anfrage erfolgreich war
    
        # JSON-Daten aus der Antwort extrahieren
        price_data = response.json()
    
        # Hier können Sie wählen, welche Daten zurückgegeben oder weiter verarbeitet werden sollen
        return price_data

    except requests.exceptions.RequestException as e:
        # Fehlerhandling für den Fall, dass die API nicht erreichbar ist oder ein anderer Fehler auftritt
        print(f"An error occurred: {e}")
        return None