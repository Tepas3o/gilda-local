"""DeferredLoadRequest ."""

from datetime import timedelta
from pydantic import BaseModel

from gilda_local.sql_config import SQLConfig


class DeferredLoadRequest(BaseModel):
    """Deferred load request message."""

    load: float | str = 0
    on_period: timedelta | str = "0:00:00"
    time_horizon: timedelta | str = "24:00:00"
    sample_frequency: timedelta | str = "0:15:00"
    co2_cost: float | str = 50  # CO2 cost [$ / gr CO2]
    kwh_cost: float | str = 150  # KWh cost [$ / KWh]

    timer_entity: str = "timer.gilda_remote_start_timer"
    co2_intensity_entity: str = "sensor.electricity_maps_co2_intensity"

    gilda_host: str = "homeassistant.local"
    gilda_opts_port: int | str = 5012
    gilda_local_port: int | str = 5024

    sql_config: SQLConfig | None = None
    sql_user: str = "homeassistant"
    sql_password: str = ""
    sql_host: str = "homeassistant.local"
    sql_database: str = "homeassistant"
    sql_port: int | str = 3306

    def get_sql_config(self):
        """Return sql config."""
        return (
            self.sql_config
            if self.sql_config is not None
            else SQLConfig(
                user=self.sql_user,
                password=self.sql_password,
                database=self.sql_database,
                host=self.sql_host,
                port=int(self.sql_port),
            )
        )
