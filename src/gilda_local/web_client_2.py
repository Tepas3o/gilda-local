"""Another web client."""

import os
import requests

# Server URL
API_URL = "http://192.168.1.85:8123/api/services/timer/start"
# API_URL = "http://127.0.0.1:5024"

API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2NGZlZjIzYTAzNmQ0YTJhOGI2NDNmYzY3MTU2OGMyNyIsImlhdCI6MTcyMjQwMzc2MCwiZXhwIjoyMDM3NzYzNzYwfQ.PF--9gieQrCSrA150E58hvZiYNUcIKA3NVf9o76UF40"  # pylint: disable=C0301 # noqa

base_url = os.environ.get("API_URL", API_URL)

headers = {"Authorization": "Bearer " + API_TOKEN}

data = {"entity_id": "timer.gilda_remote_start_timer", "duration": "0:01:23"}

response = requests.post(base_url, headers=headers, json=data, timeout=100)

print("Respuesta:", response.json())
