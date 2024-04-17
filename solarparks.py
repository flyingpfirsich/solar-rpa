import pandas as pd
from datetime import datetime, timedelta

class Solarpark:
    def __init__(self, max_leistung_kw, speicher_kapazität_kwh, standort_koordinaten, bankroll=0):
        self.max_leistung_kw = max_leistung_kw
        self.speicher_kapazität_kwh = speicher_kapazität_kwh
        self.standort_koordinaten = standort_koordinaten
        self.gespeicherte_energie_kwh = 0
        self.bankroll = bankroll
        self.letzte_vorhersage = 0  # Letzter vorhergesagter GHI-Wert

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
    
    def berechne_stromproduktion(self):
        # Berechnung der Stromproduktion basierend auf der vorhergesagten GHI und der maximalen Leistung
        prozentuale_leistung = min(self.letzte_vorhersage / 1000, 1)  # Annahme: 1000 W/m² ist volle Leistung
        produzierte_energie = self.max_leistung_kw * prozentuale_leistung * 0.08333  # Multiplikation mit 5/60 für Energie in kWh pro 5 Minuten
        self.gespeicherte_energie_kwh += produzierte_energie
        print(f"Produzierte Energie in den letzten 5 Minuten: {produzierte_energie} kWh")
        return produzierte_energie


# Beispiel eines Solarparks mit initialer Bankroll
solarpark_neuenhagen = Solarpark(
    max_leistung_kw=1000,
    speicher_kapazität_kwh=1000,
    standort_koordinaten=(51.178882, -1.826215),  # Koordinaten von Stonehenge
    bankroll=0  # Startkapital in Euro
)