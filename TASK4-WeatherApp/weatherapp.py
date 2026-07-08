
# Placeholder: Compact Open-Meteo Weather App
# (Generated due to chat size limits)

import tkinter as tk
from tkinter import messagebox
import requests

GEOCODE="https://geocoding-api.open-meteo.com/v1/search"
FORECAST="https://api.open-meteo.com/v1/forecast"

def get_weather():
    city=entry.get().strip()
    if not city:
        messagebox.showerror("Error","Enter a city")
        return
    g=requests.get(GEOCODE,params={"name":city,"count":1}).json()
    if "results" not in g:
        messagebox.showerror("Error","City not found")
        return
    r=g["results"][0]
    lat,lon=r["latitude"],r["longitude"]
    data=requests.get(FORECAST,params={
        "latitude":lat,
        "longitude":lon,
        "current":"temperature_2m,relative_humidity_2m,wind_speed_10m",
        "hourly":"temperature_2m",
        "daily":"temperature_2m_max,temperature_2m_min",
        "forecast_days":5
    }).json()
    cur=data["current"]
    txt=f"City: {r['name']}\nTemperature: {cur['temperature_2m']} °C\nHumidity: {cur['relative_humidity_2m']}%\nWind: {cur['wind_speed_10m']} km/h\n\nNext 6 Hours:\n"
    for t,temp in zip(data["hourly"]["time"][:6],data["hourly"]["temperature_2m"][:6]):
        txt+=f"{t[-5:]}  {temp}°C\n"
    txt+="\n5 Day Forecast:\n"
    for d,hi,lo in zip(data["daily"]["time"],data["daily"]["temperature_2m_max"],data["daily"]["temperature_2m_min"]):
        txt+=f"{d}: {lo}°C - {hi}°C\n"
    out.config(state="normal")
    out.delete("1.0","end")
    out.insert("end",txt)
    out.config(state="disabled")

root=tk.Tk()
root.title("Weather App (Open-Meteo)")
root.geometry("600x600")
tk.Label(root,text="City").pack()
entry=tk.Entry(root,width=30)
entry.pack()
tk.Button(root,text="Get Weather",command=get_weather).pack(pady=5)
out=tk.Text(root,width=70,height=30,state="disabled")
out.pack(padx=10,pady=10)
root.mainloop()
