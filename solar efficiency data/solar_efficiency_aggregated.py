import pandas as pd

def prepare_and_save_to_excel(input_csv_file, output_excel_file):
    # Daten einlesen
    df = pd.read_csv(input_csv_file)

    # Konvertiere 'period_end' zu datetime und extrahiere Zeit ohne Jahreszahl
    df['period_end'] = pd.to_datetime(df['period_end'])
    df['time_of_day'] = df['period_end'].dt.strftime('%m-%d %H:%M:%S')

    # Erstelle eine Spalte für das Jahr
    df['year'] = df['period_end'].dt.year

    # Pivottabelle, um jedes Jahr als eine Spalte zu haben
    pivot_df = df.pivot_table(index='time_of_day', columns='year', values='efficiency', aggfunc='first')

    # Berechnung des Durchschnitts über alle Jahre für jede Zeitperiode
    pivot_df['Durchschnitt'] = pivot_df.mean(axis=1)

    # Reset Index, um 'time_of_day' als Spalte zu haben
    pivot_df.reset_index(inplace=True)
    pivot_df.columns.name = None  # Entferne den Namen des Index/Spalten

    # Speichere das Ergebnis in einer Excel-Datei
    pivot_df.to_excel(output_excel_file, index=False)

    return pivot_df

# Beispielaufruf der Funktion
try:
    result_df = prepare_and_save_to_excel('solar efficiency/solar_efficiency_output.csv', 'solar efficiency/aggregated_solar_efficiency.xlsx')
    print("Die aggregierten Daten wurden erfolgreich in 'aggregated_solar_efficiency.xlsx' gespeichert.")
except Exception as e:
    print(str(e))
