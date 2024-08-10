"""Web client example."""

import requests

# Server URL
BASE_URL = "http://127.0.0.1:5012"


data = {
    "deferral_entity": "lavadora",
    "start_entity": "timer.gilda_remote_start_timer",
    "on_period": "1:00:00",
}

response = requests.post(f"{BASE_URL}/deferral_start", json=data, timeout=100)

print("Respuesta de Action 1:", response.json())
