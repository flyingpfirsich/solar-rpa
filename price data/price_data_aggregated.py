import pandas as pd

# Einlesen der CSV-Datei
data = pd.read_csv('price data/output.csv', parse_dates=['timestamp'])

# Hinzufügen einer neuen Spalte für den Zeitstempel ohne Jahr
data['time_of_day'] = data['timestamp'].dt.strftime('%m-%d %H:%M:%S')

# Gruppierung der Daten nach 'time_of_day' und anschließendes Pivotieren
pivot_data = data.pivot_table(index='time_of_day', columns=data['timestamp'].dt.year, values='price', aggfunc='first')

# Renaming the columns to include the year for clarity
pivot_data.columns = [str(col) for col in pivot_data.columns]

# Schreiben des transformierten DataFrames in eine Excel-Datei
pivot_data.to_excel('price data/yearly_data.xlsx')

print("Excel-Datei wurde erfolgreich erstellt.")
