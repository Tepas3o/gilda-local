"""Web server module for Gilda_local."""

import os
from datetime import timedelta
import asyncio
import logging

from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, BackgroundTasks
import requests

# from homeassistant_api import Client
# token = os.environ.get("SUPERVISOR_TOKEN", API_TOKEN)
# client = Client(API_URL, token)


HA_API_URL = "http://192.168.1.85:8123/api"
HA_API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2NGZlZjIzYTAzNmQ0YTJhOGI2NDNmYzY3MTU2OGMyNyIsImlhdCI6MTcyMjQwMzc2MCwiZXhwIjoyMDM3NzYzNzYwfQ.PF--9gieQrCSrA150E58hvZiYNUcIKA3NVf9o76UF40"  # pylint: disable=C0301 # noqa

ha_api_url = os.environ.get("HOMEASSISTANT_API", HA_API_URL)
ha_api_token = os.environ.get("SUPERVISOR_TOKEN", HA_API_TOKEN)

headers = {"Authorization": "Bearer " + ha_api_token}

logger = logging.getLogger("uvicorn")


class DeferredLoadRequest(BaseModel):
    """Deferred load request message."""

    deferred_entity: str
    on_period: timedelta
    timer_entity: str


async def async_deferred_load_process(request: DeferredLoadRequest):
    """async_deferred_load_process."""
    await asyncio.sleep(2)

    # send data to gilda_opts

    data = {"entity_id": request.timer_entity, "duration": "0:01:23"}

    start_timer_url = ha_api_url + "/services/timer/load"

    response = requests.post(start_timer_url, headers=headers, json=data, timeout=100)
    if response:
        logger.info(  #  pylint: disable=W1203
            f"gilda_local: successful load request for {data}"  # noqa
        )
    else:
        # noqa
        logger.info(  #  pylint: disable=W1203
            f"gilda_local: error response code {response.status_code}"  # noqa
        )


app = FastAPI()


@app.post("/deferred_load_request")
async def deferred_load_request(
    request: DeferredLoadRequest, background_tasks: BackgroundTasks
):
    """Deferred load process."""
    background_tasks.add_task(async_deferred_load_process, request)

    deferred_entity = request.deferred_entity
    timer_entity = request.timer_entity
    on_period = request.on_period

    return {
        "message": f"Deferred load {deferred_entity} on {on_period} and {timer_entity}"
    }


# Gilda default port
GILDALOCAL_ADDR = "0.0.0.0"
# Gilda default port
GILDALOCAL_PORT = 5024


def run():
    """Run method."""
    address = os.environ.get("GILDALOCAL_ADDR", GILDALOCAL_ADDR)
    port = int(os.environ.get("PORT", GILDALOCAL_PORT))

    uvicorn.run(app, host=address, port=port)


if __name__ == "__main__":
    run()
