import subprocess
import requests
import json
import time

FIREBASE_URL = "https://baguedor-default-rtdb.firebaseio.com"

def get_location():
    result = subprocess.run(
        ["termux-location", "-p", "network"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def send_location():
    loc = get_location()
    loc["timestamp"] = time.time()
    requests.put(f"{FIREBASE_URL}/location.json", json=loc)
    print(f"Position envoyée : {loc['latitude']}, {loc['longitude']}")

def get_command():
    res = requests.get(f"{FIREBASE_URL}/command.json")
    return res.json()

print("Agent BagueDor démarré 🔥")
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
