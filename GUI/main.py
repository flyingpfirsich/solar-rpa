import customtkinter as ctk
from tkinter import font
import threading
import logic
import time
import pytz
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

# Initialisieren des Hauptfensters
ctk.set_appearance_mode("Dark")  # Alternativ "Dark" oder "Light"
root = ctk.CTk()  # Verwendung von CTk anstelle von Tk
root.title("Solarpark Dashboard")
root.geometry("1080x720")  # Setzt die Größe des Fensters
root.resizable(False, False)  # Verhindern, dass die Fenstergröße geändert wird

# Hintergrund-Frame als Ersatz für die direkte Einstellung der Hintergrundfarbe
background_frame = ctk.CTkFrame(master=root, width=1080, height=720, corner_radius=0)
background_frame.place(x=0, y=0)
background_frame.configure(fg_color="#666666")  # Setzt die Vordergrundfarbe, die hier als Hintergrund dient

tab_frame = ctk.CTkFrame(master=root, width=205, height=720, corner_radius=0)
tab_frame.place(x=0, y=0)
tab_frame.configure(fg_color="#3F3F3F")

custom_font = font.Font(family="Inter", size=14, weight="bold")

# Label (headline_frame) erstellen mit benutzerdefinierter Schriftart
headline_label = ctk.CTkLabel(master=root, text="Solarpark \n Dashboard",
                               text_color="#FFFFFF", fg_color="#3F3F3F",
                               font=("Inter", 24, "bold"),)
headline_label.place(x=7, y=5)

#DATUM
datum_label = ctk.CTkLabel(master=root, text="Datum:",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"))
datum_label.place(x=7, y=130)

vdatum_label = ctk.CTkLabel(master=root, text="08.04.24",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"))
vdatum_label.place(x=92, y=130)

#ZEIT
zeit_label = ctk.CTkLabel(master=root, text="Zeit:",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"))
zeit_label.place(x=7, y=153)

vzeit_label = ctk.CTkLabel(master=root, text="20:20:22",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"))
vzeit_label.place(x=92, y=153)

#STATUS
status_label = ctk.CTkLabel(master=root, text="Status:",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"))
status_label.place(x=7, y=174)

vstatus_label = ctk.CTkLabel(master=root, text="inaktiv",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"))
vstatus_label.place(x=92, y=174)


#VERTRIEB
vertrieb_label = ctk.CTkLabel(master=root, text="Vertrieb:",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"))
vertrieb_label.place(x=7, y=445)

vvertrieb_label = ctk.CTkLabel(master=root, text="inaktiv",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"))
vvertrieb_label.place(x=92, y=445)

#UMSATZ
umsatz_frame = ctk.CTkFrame(master=root, width=238, height=118, corner_radius=10)
umsatz_frame.place(x=228, y=63)
umsatz_frame.configure(bg_color="#666666", fg_color="#3F3F3F")
umsatz_label = ctk.CTkLabel(master=root, text="UMSATZ",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"))
umsatz_label.place(x=303, y=65)

gesamtumsatz_label = ctk.CTkLabel(master=root, text="300,00 €",
                               text_color="#FF9417", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 34, "bold"))
gesamtumsatz_label.place(x=347, y=123, anchor="center")

#TEMPERATUR
temp_frame = ctk.CTkFrame(master=root, width=120, height=120, corner_radius=10)
temp_frame.place(x=480, y=63)
temp_frame.configure(bg_color="#666666", fg_color="#3F3F3F")
temp_label = ctk.CTkLabel(master=root, text="TEMP",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"),)
temp_label.place(x=515, y=65)
temperatur_label = ctk.CTkLabel(master=root, text="8°C",
                               text_color="#FF9417", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 34, "bold"))
temperatur_label.place(x=540, y=123, anchor="center")

#SONNE
sonne_frame = ctk.CTkFrame(master=root, width=120, height=120, corner_radius=10)
sonne_frame.place(x=611, y=63)
sonne_frame.configure(bg_color="#666666", fg_color="#3F3F3F")
sonne_label = ctk.CTkLabel(master=root, text="SONNE",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"),)
sonne_label.place(x=636, y=63)
sonnepro_label = ctk.CTkLabel(master=root, text="50%",
                               text_color="#FF9417", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 34, "bold"))
sonnepro_label.place(x=634, y=102)

#AKKU
akku_frame = ctk.CTkFrame(master=root, width=284, height=288, corner_radius=10)
akku_frame.place(x=755, y=63)
akku_frame.configure(bg_color="#666666", fg_color="#3F3F3F")
akku_label = ctk.CTkLabel(master=root, text="AKKUSTAND",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"),)
akku_label.place(x=837, y=63)


#AUSLASTUNG
leistung_frame = ctk.CTkFrame(master=root, width=238, height=144, corner_radius=10)
leistung_frame.place(x=228, y=209)
leistung_frame.configure(bg_color="#666666", fg_color="#3F3F3F")
leistung_label = ctk.CTkLabel(master=root, text="LEISTUNG",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"),)
leistung_label.place(x=295, y=211)

gesamtleistung_label = ctk.CTkLabel(master=root, text="3200 KW",
                               text_color="#FF9417", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 34, "bold"))
gesamtleistung_label.place(x=347, y=281, anchor="center")



#EFFEKTIVITÄT
effektivität_frame = ctk.CTkFrame(master=root, width=250, height=144, corner_radius=10)
effektivität_frame.place(x=480, y=209)
effektivität_frame.configure(bg_color="#666666", fg_color="#3F3F3F")
effektivität_label = ctk.CTkLabel(master=root, text="EFFEKTIVITÄT",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"),)
effektivität_label.place(x=540, y=211)


#PRODUKTION
prod_frame = ctk.CTkFrame(master=root, width=503, height=288, corner_radius=10)
prod_frame.place(x=228, y=379)
prod_frame.configure(bg_color="#666666", fg_color="#3F3F3F")
prod_label = ctk.CTkLabel(master=root, text="PRODUKTION",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"),)
prod_label.place(x=415, y=383)

#PREIS
preis_frame = ctk.CTkFrame(master=root, width=284, height=288, corner_radius=10)
preis_frame.place(x=755, y=379)
preis_frame.configure(bg_color="#666666", fg_color="#3F3F3F")
preis_label = ctk.CTkLabel(master=root, text="MARKTPREIS",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"),)
preis_label.place(x=837, y=384)


#####

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
        "max_leistung_kw": 0.32 * 23500, 
        "status":False,
        "vertrieb":False
    }

akkut_label = ctk.CTkLabel(master=root, text="Akku:",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"))
akkut_label.place(x=7, y=195)

vakkut_label = ctk.CTkLabel(master=root, text=f"{int(solarpark['gespeicherte_energie_kwh']):.1f}KWh",
                               text_color="#FFFFFF", bg_color="#3F3F3F",fg_color="#3F3F3F",
                               font=("Inter", 18, "bold"))
vakkut_label.place(x=92, y=195)

def update_dashboard():
    app_data = {
        "name": "Solarpark 1",
        "bankroll": [],
        "date": [],
        "time": [],
        "temperature": [],
        "last_day_power": [],
        "storage": {
            "stored_energy": [],
            "total_storage": 1000,
            "percentage": []
        },
        "current_power": [],
        "efficiency": []
        }
    
    while True:
        if solarpark['status']:
            solar_production = logic.get_solar_production(weather_data, solarpark)
        else:
            solar_production = 0

        price_data = logic.get_price_data(solarpark)
        weather_data = logic.get_weather_data(solarpark)
          # Include solarpark here

        if solarpark["gespeicherte_energie_kwh"]+solar_production<=solarpark['speicher_kapazität_kwh']:
            solarpark['gespeicherte_energie_kwh'] += solar_production
        else:
            solarpark["gespeicherte_energie_kwh"]=solarpark['speicher_kapazität_kwh']


        current_price, yesterday_price, decision = logic.price_decision(price_data, solarpark)
        
        if solarpark['vertrieb']:
            _ = logic.trade(price_data, solarpark)

        # Update GUI data
        current_datetime = datetime.datetime.now(pytz.timezone("Europe/Berlin"))
        current_temperature = weather_data["weather"][-1]['temperature'] if 'weather' in weather_data else 'N/A'
        storage_fill_percentage = (solarpark['gespeicherte_energie_kwh'] / solarpark['speicher_kapazität_kwh']) * 100
        power_efficiency = (solar_production / solarpark['max_leistung_kw']) if solarpark['max_leistung_kw'] > 0 else 0

        app_data["bankroll"] = solarpark["bankroll"]
        app_data["date"] = current_datetime.strftime('%Y-%m-%d')
        app_data["time"] = logic.update_data_list(app_data["time"], current_datetime.strftime('%H:%M:%S'))
        app_data["temperature"] = weather_data["weather"][-1]['temperature'] if 'weather' in weather_data else 'N/A'
        app_data["last_day_power"] = logic.update_data_list(app_data["last_day_power"], price_data['price'][-1] if 'price' in price_data else 'N/A')
        app_data["storage"]["stored_energy"] = logic.update_data_list(app_data["storage"]["stored_energy"], solarpark['gespeicherte_energie_kwh'])
        app_data["storage"]["percentage"] = logic.update_data_list(app_data["storage"]["percentage"], (solarpark['gespeicherte_energie_kwh'] / app_data["storage"]["total_storage"]) * 100)
        app_data["current_power"] = logic.update_data_list(app_data["current_power"], solar_production*100)
        app_data["efficiency"] = logic.update_data_list(app_data["efficiency"], (solar_production / solarpark['max_leistung_kw']) * 10000 if solarpark['max_leistung_kw'] > 0 else 0)
                
        #GUI Update
        vdatum_label.configure(text=str(app_data['date']))
        vzeit_label.configure(text=str(app_data["time"][-1]))
        vakkut_label.configure(text=f"{solarpark['gespeicherte_energie_kwh']:.1f}KWh")

        gesamtumsatz_label.configure(text=f"{app_data['bankroll']:.2f}€")
        temperatur_label.configure(text=f"{int(app_data['temperature'])}°C")
        sonnepro_label.configure(text="55%")
        gesamtleistung_label.configure(text=f"{app_data['current_power'][-1]:.1f} KW")
        
        #Akku Plot
        akku_fig = Figure(figsize=(2.6, 2.6), facecolor="#3F3F3F")
        akku_fig.text(x=0.05,y=0.95, s="%", color='#FFFFFF', fontsize=14,transform=akku_fig.transFigure, ha='center', va='center')
        akku_ax = akku_fig.add_subplot()
        akku_ax.set_ylim(0,100)
        akku_ax.xaxis.set_major_locator(MaxNLocator(3))
        akku_ax.text(app_data['time'][-1], app_data['storage']['percentage'][-1], f"{(app_data['storage']['percentage'][-1]):.1f}%", color='#FF9417', verticalalignment='bottom', horizontalalignment='right', fontsize=11)
        akku_ax.set_ylabel(ylabel='%')
        akku_ax.spines['top'].set_visible(False)
        akku_ax.spines['right'].set_visible(False)
        akku_ax.spines['left'].set_color('white')
        akku_ax.spines['bottom'].set_color('white')
        akku_ax.set_facecolor("#3F3F3F")
        akku_ax.tick_params(labelsize=9, colors='#FFFFFF')
        akku_ax.plot(app_data['time'], app_data['storage']['percentage'], color='#FF9417')
        akku_ax.fill_between(app_data['time'], app_data['storage']['percentage'], color='#FF9417', alpha=0.2)
        akku_canvas = FigureCanvasTkAgg(figure=akku_fig, master=root)
        akku_canvas.draw()
        akku_canvas.get_tk_widget().place(x=767, y=90)
        
        #Produktion
        prod_fig = Figure(figsize=(4.3, 2.6), facecolor="#3F3F3F")
        prod_fig.text(x=0.08,y=0.95, s="KW", color='#FFFFFF', fontsize=14,transform=prod_fig.transFigure, ha='center', va='center')
        prod_ax = prod_fig.add_subplot()
        prod_ax.set_ylim(0,(0.32 * 23500))
        prod_ax.xaxis.set_major_locator(MaxNLocator(4))
        prod_ax.text(app_data['time'][-1], app_data['current_power'][-1], f"{app_data['current_power'][-1]:.1f}KW", color='#FF9417', verticalalignment='bottom', horizontalalignment='right', fontsize=11)
        prod_ax.spines['top'].set_visible(False)
        prod_ax.spines['right'].set_visible(False)
        prod_ax.spines['left'].set_color('white')
        prod_ax.spines['bottom'].set_color('white')
        prod_ax.set_facecolor("#3F3F3F")
        prod_ax.tick_params(labelsize=9, colors='#FFFFFF')
        prod_ax.plot(app_data['time'], app_data['current_power'], color='#FF9417')
        prod_ax.fill_between(app_data['time'], app_data['current_power'], color='#FF9417', alpha=0.2)
        prod_canvas = FigureCanvasTkAgg(figure=prod_fig, master=root)
        prod_canvas.draw()
        prod_canvas.get_tk_widget().place(x=260, y=406)
        
        #Effektivität
        eff_fig = Figure(figsize=(2.2, 0.9), facecolor="#3F3F3F")
        eff_ax = eff_fig.add_subplot()
        eff_ax.set_ylim(0,100)
        eff_ax.xaxis.set_major_locator(MaxNLocator(4))
        eff_ax.text(app_data['time'][-1], app_data['efficiency'][-1], f"{app_data['efficiency'][-1]:.1f}%", color='#FF9417', verticalalignment='bottom', horizontalalignment='right', fontsize=11)
        eff_ax.spines['top'].set_visible(False)
        eff_ax.spines['right'].set_visible(False)
        eff_ax.spines['left'].set_color('white')
        eff_ax.spines['bottom'].set_color('white')
        eff_ax.set_facecolor("#3F3F3F")
        eff_ax.tick_params(labelsize=7, colors='#FFFFFF')
        eff_ax.plot(app_data['time'], app_data['efficiency'], color='#FF9417')
        eff_ax.fill_between(app_data['time'], app_data['efficiency'], color='#FF9417', alpha=0.2)
        eff_canvas = FigureCanvasTkAgg(figure=eff_fig, master=root)
        eff_canvas.draw()
        eff_canvas.get_tk_widget().place(x=493, y=246)

        #MARKT
        markt_fig = Figure(figsize=(2.6, 2.6), facecolor="#3F3F3F")
        markt_fig.text(x=0.08,y=0.95, s="€", color='#FFFFFF', fontsize=14,transform=markt_fig.transFigure, ha='center', va='center')
        markt_ax = markt_fig.add_subplot()
        markt_ax.xaxis.set_major_locator(MaxNLocator(3))
        markt_ax.text(['Heute'], current_price, f"{current_price:.1f}€", color='#FF9417', verticalalignment='bottom', horizontalalignment='right', fontsize=11)
        markt_ax.text(['Gestern'], yesterday_price, f"{yesterday_price:.1f}€", color='#FF9417', verticalalignment='bottom', horizontalalignment='right', fontsize=11)
        markt_ax.spines['top'].set_visible(False)
        markt_ax.spines['right'].set_visible(False)
        markt_ax.spines['left'].set_color('white')
        markt_ax.spines['bottom'].set_color('white')
        markt_ax.set_facecolor("#3F3F3F")
        markt_ax.tick_params(labelsize=9, colors='#FFFFFF')
        markt_ax.plot(['','Gestern','Heute'], [yesterday_price,yesterday_price, current_price], color='#FF9417', marker='.')
        #markt_ax.fill_between([0,1], [yesterday_price, current_price], color='#FF9417', alpha=0.2)
        markt_canvas = FigureCanvasTkAgg(figure=markt_fig, master=root)
        markt_canvas.draw()
        markt_canvas.get_tk_widget().place(x=767, y=406)
    
        time.sleep(0.5)


def start():
    solarpark['status'] = True
    vstatus_label.configure(text='aktiv')

def stop():
    solarpark['status'] = False
    vstatus_label.configure(text='inaktiv')

def market():
    if solarpark['vertrieb']:
        _ = logic.trade(logic.get_price_data(solarpark), solarpark, sell_all=True)
    else:    
        vvertrieb_label.configure(text='aktiv')
        solarpark['vertrieb'] = True
        markt_button.configure(text='CLEAR')

def halten():
    solarpark['vertrieb'] = False
    vvertrieb_label.configure(text=f"inaktiv")
    markt_button.configure(text='VERKAUFEN')



markt_button = ctk.CTkButton(master=root, width=164, height=55, corner_radius=10, text="VERKAUFEN", font=("Inter", 16, "bold"), command=market, hover_color='#ba7b32')
markt_button.place(x=13, y=379)
markt_button.configure(bg_color="#3F3F3F", fg_color="#A95B00")

halten_button = ctk.CTkButton(master=root, width=164, height=55, corner_radius=10, text="HALTEN", font=("Inter", 16, "bold"), command=halten, hover_color='#ba7b32')
halten_button.place(x=13, y=308)
halten_button.configure(bg_color="#3F3F3F", fg_color="#A95B00")

start_button = ctk.CTkButton(master=root, width=164, height=55, corner_radius=10, text="START", font=("Inter", 16, "bold"), command=start, hover_color='#ba7b32')
start_button.place(x=13, y=541)
start_button.configure(bg_color="#3F3F3F", fg_color="#A95B00")

stop_button = ctk.CTkButton(master=root, width=164, height=55, corner_radius=10, text="STOP", font=("Inter", 16, "bold"), command=stop, hover_color='#ba7b32')
stop_button.place(x=13, y=612)
stop_button.configure(bg_color="#3F3F3F", fg_color="#A95B00")


thread = threading.Thread(target=update_dashboard)
thread.daemon = True
thread.start()

# Die Hauptloop starten
root.mainloop()
