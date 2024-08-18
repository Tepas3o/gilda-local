"""DeferredLoadRequest ."""

from datetime import timedelta
from pydantic import BaseModel, Field

from gilda_local.sql_config import SQLConfig


class DeferredLoadRequest(BaseModel):
    """Deferred load request message."""

    deferred_entity: str = ""
    load: float = 0
    on_period: timedelta | str = "0:00:00"

    timer_entity: str = ""
    timer_api_url: str = ""
    timer_api_token: str = ""

    sql_config: SQLConfig = Field(default_factory=SQLConfig)

    gilda_opts_host: str = "homeassistant.local"
    gilda_opts_port: int = "5012"

    co2_intensity_entity: str = "sensor.electricity_maps_co2_intensity"

    # CO2 cost [$ / gr CO2]
    co2_cost: float = 50

    # KWh cost [$ / KWh]
    kwh_cost: float = 150

    time_horizont: timedelta | str = "24:00:00"
    sample_frequency: timedelta | str = "0:15:00"
