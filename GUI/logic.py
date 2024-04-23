import requests
import datetime
import pytz
import time
import json
import customtkinter as ctk
import threading

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


def get_solar_production(weather_data, solarpark):
    # Modulfläche und Modulanzahl aus dem solarpark Dictionary abrufen
    module_area = solarpark['Modulgröße_m2']
    num_modules = solarpark['Modulanzahl']

    # Gesamtfläche aller Module berechnen
    total_module_area = module_area * num_modules

    # Solarstrahlung aus den Wetterdaten abrufen, die als kWh/m² angegeben wird
    solar_irradiance = weather_data["weather"][-1]["solar"]  # Solarstrahlung in kWh/m²
    cloud_cover = weather_data["weather"][-1]["cloud_cover"]
    sun_intensity = 100 - cloud_cover
    if int(sun_intensity) <= 50:
        emoji = "⛅️"
    else:
        emoji = "☀️"


    # Gesamte auf die Module eingestrahlte Energie berechnen
    total_solar_input_kwh = solar_irradiance * total_module_area  # in kWh

    # Berechnung der tatsächlich produzierten Energie basierend auf dem Modulwirkungsgrad
    energy_produced_kwh = total_solar_input_kwh * solarpark['Modulwirkungsgrad']
    energy_5s = (energy_produced_kwh / 3600) * 5

    return energy_5s, sun_intensity, emoji


def price_decision(price_data, solarpark):
    # Aktuelle Zeit in UTC holen und auf die nächste volle Stunde runden
    now = datetime.datetime.utcnow()
    rounded_now = now.replace(minute=0, second=0, microsecond=0)
    if now.minute >= 30:  # Runden zur nächsten vollen Stunde, falls Minute >= 30
        rounded_now += datetime.timedelta(hours=1)
    
    # Zeitstempel von gestern zur selben Stunde
    rounded_yesterday = rounded_now - datetime.timedelta(days=1)

    # Unix Timestamps in Sekunden umrechnen
    current_unix = int(rounded_now.timestamp())
    yesterday_unix = int(rounded_yesterday.timestamp())

    # Finde die Indizes der relevanten Zeitstempel
    try:
        current_index = price_data['unix_seconds'].index(current_unix)
        yesterday_index = price_data['unix_seconds'].index(yesterday_unix)
        
        # Hole die aktuellen und gestrigen Preise
        current_price = price_data['price'][current_index]
        yesterday_price = price_data['price'][yesterday_index]
        # Entscheidung treffen
        if solarpark['gespeicherte_energie_kwh'] >= 0.8 * solarpark['speicher_kapazität_kwh']:
            return float(current_price), float(yesterday_price), "sell"
        elif current_price > yesterday_price:
            return float(current_price), float(yesterday_price), "sell"
        else:
            return current_price, yesterday_price, "hold"
    except ValueError:
        # Fehlerbehandlung, falls die Zeitstempel nicht in den Daten gefunden werden
        return 0,0,"Error: Timestamp not found in price data"


def trade(price_data, solarpark, sell_all=False):
    # Treffen der Entscheidung zum Verkaufen oder Halten
    _,_,decision = price_decision(price_data, solarpark)
    
    if decision == "sell":
        # Ermittle den aktuellen Preis basierend auf der nächsten vollen Stunde
        now = datetime.datetime.utcnow()
        rounded_now = now.replace(minute=0, second=0, microsecond=0)
        if now.minute >= 30:
            rounded_now += datetime.timedelta(hours=1)

        # Finde den entsprechenden Unix-Timestamp
        current_unix = int(rounded_now.timestamp())
        current_index = price_data['unix_seconds'].index(current_unix)
        current_price = price_data['price'][current_index]

        try:
            # Entscheidung, wie viel verkauft werden soll, basierend auf sell_all
            if sell_all:
                amount_to_sell = solarpark['gespeicherte_energie_kwh']
            else:
                amount_to_sell = 0.03 * solarpark['gespeicherte_energie_kwh']

            # Aktualisieren der gespeicherten Energie und der Bankroll wie zuvor
            solarpark['gespeicherte_energie_kwh'] -= amount_to_sell
            revenue = amount_to_sell * current_price / 1000  # Umrechnung von EUR/MWh in EUR/kWh
            solarpark['bankroll'] += revenue
            
            return f"Sold {amount_to_sell} kWh at {current_price} EUR/MWh, added {revenue} EUR to bankroll. New bankroll: {solarpark['bankroll']} EUR"
        
        except ValueError:
            # Fehlerbehandlung bleibt gleich
            return "Error: Current timestamp not found in price data"
    
    else:
        # Keine Aktion, bleibt unverändert
        return "No action taken, hold position."


def update_data_list(data_list, new_value):
    data_list.append(new_value)
    if len(data_list) > 20:
        data_list.pop(0)  # Entfernt den ältesten Wert
    return data_list

