"""Web client example."""

import requests

# Server URL
BASE_URL = "http://192.168.1.85:5024"


data = {
    "deferral_entity": "lavadora",
    "start_entity": "timer.gilda_remote_start_timer",
    "on_period": "1:00:00",
}

response = requests.post(f"{BASE_URL}/deferral_start", json=data, timeout=100)

print("Respuesta:", response.json())
