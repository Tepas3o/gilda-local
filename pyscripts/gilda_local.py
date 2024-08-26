"""Gilda local pyscript services/actions."""

import logging
import requests

logger = logging.getLogger("pyscript_gilda_local")

GILDA_LOCAL_URL = "http://homeassistant.local:5024"


@service  # pylint: disable=E0602 # noqa
def gilda_deferred_load_request(
    trigger_type=None,  # pylint: disable=W0613
    context=None,  # pylint: disable=W0613
    gilda_local_url=GILDA_LOCAL_URL,
    **data,
):
    """Gilda deferred load request."""
    logger.info("deferred load request data: %s", data)

    resp = task.executor(  # pylint: disable=E0602 # noqa
        requests.post,
        f"{gilda_local_url}/deferred_load_request",
        json=data,
        timeout=10,
    )

    logger.info("elapsed time: %s", resp.elapsed)
    if resp.status_code == 200:
        logger.info("response content: %s", resp.json())
    else:
        logger.error("bad status code: %s", resp.status_code)
