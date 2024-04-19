import pandas as pd

def calculate_solar_efficiency(csv_file_path, output_csv_file_path):
    # Daten laden
    df = pd.read_csv(csv_file_path)
    
    # Sicherstellen, dass alle notwendigen Spalten vorhanden sind
    required_columns = ['period_end', 'ghi', 'clearsky_ghi']
    if not all(column in df.columns for column in required_columns):
        raise ValueError("Die notwendigen Spalten sind nicht im DataFrame vorhanden.")

    # Berechnung der Effizienz
    # Vermeide Division durch Null, indem du einen kleinen Wert zu clearsky_ghi hinzufügst
    df['efficiency'] = df['ghi'] / (df['clearsky_ghi'] + 0.001)
    
    # Effizienz normalisieren, um sicherzustellen, dass sie zwischen 0 und 1 liegt
    df['efficiency'] = df['efficiency'].clip(0, 1)

    # Selektiere nur die relevanten Spalten für die Ausgabe
    output_df = df[['period_end', 'ghi', 'clearsky_ghi', 'efficiency']]
    
    # Speichere das Ergebnis in einer neuen CSV-Datei
    output_df.to_csv(output_csv_file_path, index=False)

    return output_df

# Beispielaufruf der Funktion
try:
    efficiency_df = calculate_solar_efficiency('solar efficiency/solar_data.csv', 'solar_efficiency_output.csv')
    print("Die Ergebnisse wurden erfolgreich in 'solar_efficiency_output.csv' gespeichert.")
except Exception as e:
    print(str(e))
