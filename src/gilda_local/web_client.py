import requests

# URL base del servidor
base_url = "http://127.0.0.1:8000"


data = {"deferral_entity": "lavadora",
        "start_entity":"timer.gilda_remote_start_timer",
        "on_period":"1:00:00",
        }

response = requests.post(f"{base_url}/deferral_start", json=data)

print("Respuesta de Action 1:", response.json())




