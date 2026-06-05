import requests
import json
import sys
import time

FIREBASE_URL = "https://baguedor-default-rtdb.firebaseio.com"
PASSWORD = "baguedor2026"

def auth():
    pwd = input("🔐 Mot de passe : ")
    if pwd != PASSWORD:
        print("⛔ Accès refusé")
        sys.exit()

def get_address(lat, lng):
    try:
        res = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lng, "format": "json"},
            headers={"User-Agent": "BagueDor/1.0"}
        )
        return res.json().get("display_name", "Adresse inconnue")
    except:
        return "Adresse inconnue"

def start():
    requests.put(f"{FIREBASE_URL}/command.json", json="start")
    print("✅ Tracking démarré")

def stop():
    requests.put(f"{FIREBASE_URL}/command.json", json="stop")
    print("🛑 Tracking arrêté")

def status():
    res = requests.get(f"{FIREBASE_URL}/location.json")
    data = res.json()
    if not data:
        print("❌ Aucune position disponible")
        return
    t = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(data["timestamp"]))
    adresse = get_address(data["latitude"], data["longitude"])
    print(f"📍 Latitude  : {data['latitude']}")
    print(f"📍 Longitude : {data['longitude']}")
    print(f"🏠 Adresse   : {adresse}")
    print(f"⏱  Timestamp : {t}")
    print(f"🎯 Précision : {data['accuracy']}m")

commands = {"start": start, "stop": stop, "status": status}

auth()

if len(sys.argv) < 2 or sys.argv[1] not in commands:
    print("Usage: python cli.py [start|stop|status]")
    sys.exit()

commands[sys.argv[1]]()
