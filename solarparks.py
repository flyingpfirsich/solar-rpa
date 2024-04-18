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

    def update_vorhersage(self, model, features):
        # Vorhersage für den aktuellen Zeitpunkt machen
        self.letzte_vorhersage = model.predict([features])[0]
        print(f"Aktuelle GHI Vorhersage: {self.letzte_vorhersage} W/m²")


    def vorhersage_stromproduktion(self):
        date = datetime.now()
        last_date = date + timedelta(hours=12)
        produzierte_energie = 0
        solarvalues = weatherforecast.berechne_solar_intensität(date,last_date)
        for value in solarvalues:
            produzierte_energie += value * self.fläche
        print(produzierte_energie)

    def berechne_stromproduktion(self):
        date = datetime.now()
        last_date = date + timedelta(hours=1)
        #solar Intensität berechnen
        solar_intensität = weatherforecast.berechne_solar_intensität(date, last_date)
    
        #prozentuale_leistung = min(self.letzte_vorhersage / 1000, 1)  # Annahme: 1000 W/m² ist volle Leistung
        produzierte_energie = solar_intensität[0] * self.fläche
        self.gespeicherte_energie_kwh += produzierte_energie
        print(f"Es wird so viel Energie produziert: {produzierte_energie} ")
        print(f"Produzierte Energie in den letzten 5 Minuten: {produzierte_energie} kWh")
        return produzierte_energie

