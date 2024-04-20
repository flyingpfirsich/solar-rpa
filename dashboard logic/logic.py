import requests
import datetime
import pytz
import time
import json
import customtkinter as ctk
import threading

solarpark = {
    "name": "Solarpark Neuenhagen",
    "speicher_kapazität_kwh": 22000,
    "standort_koordinaten": (51.178882, -1.826215),
    "gespeicherte_energie_kwh": 0,
    "bankroll": 0,
    "Modulenennleistung_kW": 0.32,
    "Modulgröße_m2": 1.7,
    "Modulanzahl": 23500,
    "Modulwirkungsgrad": 0.22,
    "max_leistung_kw": 0.32 * 23500  # Modulnennleistung_kW * Modulanzahl
}


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
        # API-Aufruf durchführen
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

    # Gesamte auf die Module eingestrahlte Energie berechnen
    total_solar_input_kwh = solar_irradiance * total_module_area  # in kWh

    # Berechnung der tatsächlich produzierten Energie basierend auf dem Modulwirkungsgrad
    energy_produced_kwh = total_solar_input_kwh * solarpark['Modulwirkungsgrad']
    energy_5s = (energy_produced_kwh / 3600) * 5

    return energy_5s


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
            return "sell"
        elif current_price > yesterday_price:
            return "sell"
        else:
            return "hold"
    except ValueError:
        # Fehlerbehandlung, falls die Zeitstempel nicht in den Daten gefunden werden
        return "Error: Timestamp not found in price data"


def trade(price_data, solarpark):
    # Treffen der Entscheidung zum Verkaufen oder Halten
    decision = price_decision(price_data, solarpark)
    
    if decision == "sell":
        # Ermittle den aktuellen Preis basierend auf der nächsten vollen Stunde
        now = datetime.datetime.utcnow()
        rounded_now = now.replace(minute=0, second=0, microsecond=0)
        if now.minute >= 30:
            rounded_now += datetime.timedelta(hours=1)

        # Finde den entsprechenden Unix-Timestamp
        current_unix = int(rounded_now.timestamp())

        try:
            # Index des aktuellen Timestamps finden
            current_index = price_data['unix_seconds'].index(current_unix)
            current_price = price_data['price'][current_index]
            
            # 3% der gespeicherten Energie verkaufen
            amount_to_sell = 0.03 * solarpark['gespeicherte_energie_kwh']
            solarpark['gespeicherte_energie_kwh'] -= amount_to_sell
            
            # Gewinn berechnen und zur Bankroll hinzufügen
            revenue = amount_to_sell * current_price / 1000  # Umrechnung von EUR/MWh in EUR/kWh
            solarpark['bankroll'] += revenue
            
            return f"Sold {amount_to_sell} kWh at {current_price} EUR/MWh, added {revenue} EUR to bankroll. New bankroll: {solarpark['bankroll']} EUR"
        
        except ValueError:
            # Fehlerbehandlung, falls der Timestamp nicht gefunden wird
            return "Error: Current timestamp not found in price data"
    
    else:
        return "No action taken, hold position."


'''while True:
    price_data = get_price_data(solarpark)
    weather_data = get_weather_data(solarpark)
    solar_production = get_solar_production()
    solarpark['gespeicherte_energie_kwh'] += solar_production
    decision = price_decision(price_data, solarpark)
    trade_result = trade(price_data, solarpark)

    # Erstellen eines JSON-Objekts mit den gewünschten Daten
    current_datetime = datetime.datetime.now(pytz.timezone("Europe/Berlin"))
    current_temperature = weather_data["weather"][-1]['temperature'] if 'weather' in weather_data else 'N/A'
    storage_fill_percentage = (solarpark['gespeicherte_energie_kwh'] / solarpark['speicher_kapazität_kwh']) * 100
    power_efficiency = (solar_production / solarpark['max_leistung_kw']) if solarpark['max_leistung_kw'] > 0 else 0

    data_to_print = {
        "Name des Solarparks": solarpark["name"],
        "Aktuelle Bankroll": solarpark["bankroll"],
        "Heutiger Tag": current_datetime.strftime('%Y-%m-%d'),
        "Aktuelle Uhrzeit": current_datetime.strftime('%H:%M:%S'),
        "Aktuelle Temperatur": current_temperature,
        "Stromdaten des letzten Tages": price_data['price'][-1] if 'price' in price_data else 'N/A',
        "Fülle des Speichers": {
            "Gespeicherte Energiemenge (kWh)": solarpark['gespeicherte_energie_kwh'],
            "Gesamtspeicher (kWh)": solarpark['speicher_kapazität_kwh'],
            "Prozentsatz": storage_fill_percentage
        },
        "Aktuelle Leistung des Solarparks (kW)": solar_production,
        "Effektivität des Solarparks (%)": power_efficiency * 100
    }

    # Ausgabe der gesammelten Daten
    print(json.dumps(data_to_print, indent=4))

    time.sleep(5)  # Pause, um die Schleife alle 5 Sekunden zu wiederholen'''


def update_dashboard():
    while True:
        price_data = get_price_data(solarpark)
        weather_data = get_weather_data(solarpark)
        solar_production = get_solar_production(weather_data, solarpark)  # Include solarpark here
        solarpark['gespeicherte_energie_kwh'] += solar_production
        decision = price_decision(price_data, solarpark)
        trade_result = trade(price_data, solarpark)

        # Update GUI data
        current_datetime = datetime.datetime.now(pytz.timezone("Europe/Berlin"))
        current_temperature = weather_data["weather"][-1]['temperature'] if 'weather' in weather_data else 'N/A'
        storage_fill_percentage = (solarpark['gespeicherte_energie_kwh'] / solarpark['speicher_kapazität_kwh']) * 100
        power_efficiency = (solar_production / solarpark['max_leistung_kw']) if solarpark['max_leistung_kw'] > 0 else 0

        app_data = {
            "name": solarpark["name"],
            "bankroll": solarpark["bankroll"],
            "date": current_datetime.strftime('%Y-%m-%d'),
            "time": current_datetime.strftime('%H:%M:%S'),
            "temperature": current_temperature,
            "last_day_power": price_data['price'][-1] if 'price' in price_data else 'N/A',
            "storage": {
                "stored_energy": solarpark['gespeicherte_energie_kwh'],
                "total_storage": solarpark['speicher_kapazität_kwh'],
                "percentage": storage_fill_percentage
            },
            "current_power": solar_production,
            "efficiency": power_efficiency * 100
        }

        for key, value in app_data.items():
            if isinstance(value, dict):
                labels[key].configure(text=f"{value['stored_energy']} / {value['total_storage']} kWh ({value['percentage']}%)")
            else:
                labels[key].configure(text=value)

        time.sleep(5)  # Refresh data every 5 seconds



# GUI setup
app = ctk.CTk()
app.title("Solarpark Dashboard")
app.geometry("800x600")

labels = {}
data_keys = ["name", "bankroll", "date", "time", "temperature", "last_day_power", "storage", "current_power", "efficiency"]
for i, key in enumerate(data_keys):
    frame = ctk.CTkFrame(app)
    frame.pack(pady=10, padx=10, fill="x")
    label = ctk.CTkLabel(frame, text=key.replace("_", " ").title() + ":")
    label.pack(side="left")
    value_label = ctk.CTkLabel(frame, text="")
    value_label.pack(side="right")
    labels[key] = value_label

# Thread zum Aktualisieren der GUI
thread = threading.Thread(target=update_dashboard)
thread.daemon = True
thread.start()

# Starten der GUI
app.mainloop()
