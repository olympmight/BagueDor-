import subprocess
import requests
import json
import time
import os
import uuid

FIREBASE_URL = "https://baguedor-default-rtdb.firebaseio.com"
ID_FILE = os.path.expanduser("~/.baguedor_id")

def get_device_id():
    if os.path.exists(ID_FILE):
        with open(ID_FILE, "r") as f:
            return f.read().strip()
    device_id = "device_" + uuid.uuid4().hex[:6]
    with open(ID_FILE, "w") as f:
        f.write(device_id)
    print(f"🆔 Nouvel ID généré : {device_id}")
    print(f"📤 Envoie cet ID à ton admin pour être protégé !")
    return device_id

DEVICE_ID = get_device_id()

def get_location():
    result = subprocess.run(
        ["termux-location", "-p", "network"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def send_location():
    loc = get_location()
    loc["timestamp"] = time.time()
    requests.put(f"{FIREBASE_URL}/devices/{DEVICE_ID}/location.json", json=loc)
    print(f"[{DEVICE_ID}] Position envoyée : {loc['latitude']}, {loc['longitude']}")

def get_command():
    res = requests.get(f"{FIREBASE_URL}/devices/{DEVICE_ID}/command.json")
    return res.json()

print(f"Agent BagueDor démarré 🔥 [{DEVICE_ID}]")
while True:
    try:
        command = get_command()
        print(f"Commande : {command}")
        if command == "start":
            send_location()
        else:
            print("En attente de commande start...")
    except Exception as e:
        print("Erreur :", e)
    time.sleep(10)
