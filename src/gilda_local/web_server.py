"""Web server module for Gilda_local."""

import asyncio
import logging
import os
from datetime import timedelta

import mariadb
import requests
import uvicorn
from fastapi import BackgroundTasks, FastAPI

from gilda_local.deferred_load import DeferredLoad, DeferredLoadRequest

ha_api_url = os.environ.get("SUPERVISOR_API", "http://supervisor/core/api")
ha_api_token = os.environ.get("SUPERVISOR_TOKEN", "")


logger = logging.getLogger("uvicorn")


async def async_deferred_load_process(request: DeferredLoadRequest):
    """async_deferred_load_process."""
    await asyncio.sleep(2)

    # send data to gilda_opts

    logger.info("async_deferred_load_request: %s", request)

    try:
        deferred_load = DeferredLoad(request, logger)
        on_delay = deferred_load.get_on_delay()
    except mariadb.Error as e:
        logger.error("async_deferred_load_process: mariadb issue %s", e)
        on_delay = timedelta(hours=0)
    except Exception as e:  # pylint: disable=W0718
        logger.error("async_deferred_load_process: computing the on_delay %s", e)
        on_delay = timedelta(hours=0)

    logger.info("async_deferred_load_process: calculated on_delay of %s", on_delay)

    start_timer_url = f"{ha_api_url}/services/timer/start"
    headers = {"Authorization": f"Bearer {ha_api_token}"}
    data = {"entity_id": request.timer_entity, "duration": str(on_delay)}

    if len(data["entity_id"]) == 0:
        logger.info("async_deferred_load_process: no timer entity to start %s", data)
        return

    logger.info("async_deferred_load_process: setting timer url: %s", start_timer_url)
    logger.info("async_deferred_load_process: setting timer headers: %s", headers)
    logger.info("async_deferred_load_process: calling timer data: %s", data)

    response = requests.post(start_timer_url, headers=headers, json=data, timeout=100)
    if response:
        logger.info(
            "async_deferred_load_process: : successful load request for %s", data
        )
    else:
        logger.error(
            "async_deferred_load_process: : bad response status code %s",
            response.status_code,
        )


app = FastAPI()


@app.post("/deferred_load_request")
async def deferred_load_request(data: dict, background_tasks: BackgroundTasks):
    """Deferred load process."""
    logger.info("deferred_load_process: request dict: %s", data)

    request = DeferredLoadRequest(**data)

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
    if len(ha_api_token) == 0:
        logger.error("run: unknown API Token, shutting down.")
        return

    address = os.environ.get("ADDRESS", GILDALOCAL_ADDR)
    port = int(os.environ.get("PORT", f"{GILDALOCAL_PORT}"))

    uvicorn.run(app, host=address, port=port)


if __name__ == "__main__":
    run()
