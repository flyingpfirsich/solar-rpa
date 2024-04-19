import pandas as pd

# Einlesen der Daten aus der JSON-Datei
with open('price data/price_data.json', 'r') as file:
    data = pd.read_json(file)

# Umwandlung der UNIX-Zeitstempel in lesbare Datums-/Zeitformate
data['timestamp'] = pd.to_datetime(data['unix_seconds'], unit='s')

# Auswahl der Spalten 'timestamp' und 'price'
data = data[['timestamp', 'price']]

# Schreiben des DataFrames in eine CSV-Datei
data.to_csv('price data/output.csv', index=False)

print("CSV-Datei wurde erfolgreich erstellt.")
