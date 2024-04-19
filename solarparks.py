import pandas as pd
from datetime import datetime, timedelta
import weatherforecast

class Solarpark:
    def __init__(self, max_leistung_kw, speicher_kapazität_kwh, standort_koordinaten, bankroll=0, fläche=100):
        self.max_leistung_kw = max_leistung_kw
        self.speicher_kapazität_kwh = speicher_kapazität_kwh
        self.standort_koordinaten = standort_koordinaten
        self.gespeicherte_energie_kwh = 0
        self.bankroll = bankroll
        self.fläche = fläche

    def hinzufügen_geld(self, betrag):
        self.bankroll += betrag
        print(f"Bankroll erhöht um {betrag} Euro. Neuer Stand: {self.bankroll} Euro.")
    
    def abziehen_geld(self, betrag):
        if betrag > self.bankroll:
            print("Nicht genügend Geld vorhanden.")
        else:
            self.bankroll -= betrag
            print(f"Bankroll verringert um {betrag} Euro. Neuer Stand: {self.bankroll} Euro.")

    def berechne_maxAuslastung(self):
        i = 1
        while(self.gespeicherte_energie_kwh<self.speicher_kapazität_kwh):
            Solarpark.berechne_stromproduktion(self, zeitDelta=i)
            i += 1
        print(f"Die maximale Auslastung wird in {i} Stunden erreicht")
        return i


    def berechne_stromproduktion(self, zeitDelta):
        produzierte_energie = 0
        date = datetime.now()
        last_date = date + timedelta(hours=zeitDelta)
        #solar Intensität berechnen
        solar_intensitäten = weatherforecast.berechne_solar_intensität(date, last_date)
        print(f"Die aktuelle Solar-Intensität beträgt {solar_intensitäten[0]}")

        for value in solar_intensitäten:
            produzierte_energie += value * self.fläche

        self.gespeicherte_energie_kwh += produzierte_energie
        print(f"es wird im Zeitraum von {zeitDelta}h so viel kwH produziert; {produzierte_energie}, der speicherstand: {self.gespeicherte_energie_kwh}")
        #prozentuale_leistung = min(self.letzte_vorhersage / 1000, 1)  # Annahme: 1000 W/m² ist volle Leistung
        
        return produzierte_energie

    def berechne_strom_buchwert(self, gespeicherte_energie_kwh):
        strompreis = get_strompreis()
        return strompreis * gespeicherte_energie_kwh