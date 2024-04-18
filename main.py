from solarparks import Solarpark

def main():
    solarpark_neuenhagen = Solarpark(
        max_leistung_kw=1000,
        speicher_kapazität_kwh=1000,
        standort_koordinaten=(51.178882, -1.826215),  # Koordinaten von Stonehenge
        bankroll=0, # Startkapital in Euro
        fläche=100
    )
    
    solarpark_neuenhagen.berechne_stromproduktion()
    solarpark_neuenhagen.vorhersage_stromproduktion()

if __name__ == "__main__":
    main()
