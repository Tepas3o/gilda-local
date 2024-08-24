"""DeferredLoadRequest ."""

from datetime import timedelta
from pydantic import BaseModel

from gilda_local.sql_config import SQLConfig


class DeferredLoadRequest(BaseModel):
    """Deferred load request message."""

    deferred_entity: str = ""
    load: float | str = 0
    on_period: timedelta | str = "0:00:00"

    timer_entity: str = "timer.gilda_remote_start_timer"

    sql_config: SQLConfig | None = None
    sql_user: str = "homeassistant"
    sql_password: str = ""
    sql_host: str = "homeassistant.local"
    sql_database: str = "homeassistant"
    sql_port: int | str = 3306

    gilda_opts_host: str = "homeassistant.local"
    gilda_opts_port: int | str = 5012

    co2_intensity_entity: str = "sensor.electricity_maps_co2_intensity"

    # CO2 cost [$ / gr CO2]
    co2_cost: float | str = 50

    # KWh cost [$ / KWh]
    kwh_cost: float | str= 150

    time_horizon: timedelta | str = "24:00:00"
    sample_frequency: timedelta | str = "0:15:00"

    def get_sql_config(self):
        """Return sql config."""
        return (
            self.sql_config
            if self.sql_config is not None
            else SQLConfig(
                user=DeferredLoadRequest.sql_user,
                password=DeferredLoadRequest.sql_password,
                database=DeferredLoadRequest.sql_database,
                host=DeferredLoadRequest.sql_host,
                port=DeferredLoadRequest.sql_port,
            )
        )
