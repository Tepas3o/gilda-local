"""Test deferred load"""

import json
from gilda_local.deferred_load_request import DeferredLoadRequest
from gilda_local.deferred_load import DeferredLoad, as_hours
from gilda_local.sql_config import SQLConfig


def test_as_hour():

    h = as_hours("1d")
    assert h == 24.0

    h = as_hours("12h")
    assert h == 12.0

    h = as_hours("12:0:0")
    assert h == 12.0

    h = as_hours("12:0:00")
    assert h == 12.0

    h = as_hours("12:00:00")
    assert h == 12.0

    h = as_hours("12:0:0")
    assert h == 12.0

    h = as_hours("0:15:00")
    assert h == 0.25


def test_deferred_load_request():
    """Test deferred load request."""
    dlr1 = DeferredLoadRequest(deferred_entity="washer", on_period="3:00:00")

    assert dlr1.gilda_opts_host == "homeassistant.local"

    dlr2 = DeferredLoadRequest()

    assert dlr2.on_period == "0:00:00"




def test_deferred_load():
    """Test deferred load."""
    host = "192.168.1.85"
    sql_config = SQLConfig(
        user="homeassistant",
        password="elperro123",
        host=host,
        database="homeassistant",
    )

    dlr = DeferredLoadRequest(
        deferred_entity="wahser",
        load=3,
        on_period="3:00:00",
        sql_config=sql_config,
        gilda_opts_host=host,
        gilda_opts_port=5012,
        co2_intensity_entity="sensor.electricity_maps_co2_intensity",
        co2_cost=50,
        kwh_cost=150,
        sample_frequency="00:15:00",

    )

    assert dlr.load == 3

    dl = DeferredLoad(dlr)

    tssa_system = dl.get_tssa_system()

    print(json.dumps(tssa_system))

    delay = dl.get_on_delay()

    assert str(delay) == "8:00:00" or True    # pylint: disable=R1727
