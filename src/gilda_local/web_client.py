"""Web client example."""

import os
import requests

# Server URL
BASE_URL = "http://192.168.1.85:5024"
# BASE_URL = "http://127.0.0.1:5024"

base_url = os.environ.get("BASE_URL", BASE_URL)

data = {
    "deferral_entity": "lavadora",
    "timer_entity": "timer.gilda_remote_start_timer",
    "on_period": "1:00:00",
}

response = requests.post(f"{base_url}/deferral_start", json=data, timeout=10)

print("Respuesta:", response.json())
