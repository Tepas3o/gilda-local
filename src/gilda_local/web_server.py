"""Web server module for Gilda_local."""

import os

from datetime import timedelta
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio

from homeassistant_api import Client

app = FastAPI()

api_url = "http://127.0.0.1:8123/api"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2NGZlZjIzYTAzNmQ0YTJhOGI2NDNmYzY3MTU2OGMyNyIsImlhdCI6MTcyMjQwMzc2MCwiZXhwIjoyMDM3NzYzNzYwfQ.PF--9gieQrCSrA150E58hvZiYNUcIKA3NVf9o76UF40"

client = Client(api_url, api_token)


class DeferralStartRequest(BaseModel):
    """Deferral start request message."""

    deferral_entity: str
    start_entity: str
    on_period: timedelta


async def async_deferral_start_process(request: DeferralStartRequest):
    """async_deferral_start_process."""
    await asyncio.sleep(2)

    timer_domain = client.get_domain("timer")
    timer_domain.start(entity_id=request.start_entity, duration="0:01:23")

    timer = client.get_entity(entity_id=request.start_entity)
    print("attributes", timer.state.attributes)

    # timer.start({'duration': "0:01:23"})

    state = client.set_state(timer.state)

    print("state", state)


@app.post("/deferral_start")
async def deferral_start(request: DeferralStartRequest,
                         background_tasks: BackgroundTasks):
    """deferral start process."""

    background_tasks.add_task(async_deferral_start_process, request)

    deferral_entity = request.deferral_entity
    start_entity = request.start_entity
    on_period = request.on_period

    return {"message":
            f""""Deferral start request for {deferral_entity} using on period
            {on_period} and trigger entity {start_entity}"""}


# Gilda default port
GILDALOCAL_ADDR = "0.0.0.0"
# Gilda default port
GILDALOCAL_PORT = 5024
# 400 is the HTTP status code for Bad Request
BAD_REQUEST = 400
# 200 is the HTTP status code for OK
OK_REQUEST = 200

def run():
    import uvicorn

    address = os.environ.get("GILDALOCAL_ADDR", GILDALOCAL_ADDR)
    port = int(os.environ.get("PORT", GILDALOCAL_PORT))


    uvicorn.run(app, host=address, port=port)

