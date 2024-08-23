"""Deferred load module."""

import json
from datetime import datetime, timedelta
from typing import List

import requests
from pytimeparse2 import parse as timeparse

from gilda_local.deferred_load_request import DeferredLoadRequest
from gilda_local.ha_sqlconn import HASQLConn


def as_hours(dt):
    """Convert a timedelta or str to hours."""
    return (dt.total_seconds() if isinstance(dt, timedelta) else timeparse(dt)) / 3600.0


class DeferredLoad:
    """Deferred load class."""

    def __init__(self, deferred_load_request: DeferredLoadRequest):
        """Initialize Deferred load."""
        self.deferred_load_request = deferred_load_request
        self.ha_sqlconn = HASQLConn(deferred_load_request.get_sql_config())
        self.dt = as_hours(self.deferred_load_request.sample_frequency)

    @staticmethod
    def create_tssa_system(
        deferred_load_request: DeferredLoadRequest,
        emission_factor_forecast: List[float],
        block_duration: float,
    ):
        """Create a TSSA system to optimize."""

        if block_duration < 0:
            return None

        on_period = as_hours(deferred_load_request.on_period)
        if on_period <= 0:
            return None

        n = len(emission_factor_forecast)
        if n == 0:
            return None

        system = {}
        system["name"] = "deferred_load"
        system["uid"] = 1
        system["block_durations"] = [block_duration] * n

        bus = {}
        bus["name"] = "bus"
        bus["uid"] = 1
        system["buses"] = [bus]

        grid = {}
        grid["name"] = "grid"
        grid["uid"] = 1
        grid["bus_uid"] = 1
        grid["capacity"] = deferred_load_request.load
        grid["energy_buy_price_sched"] = deferred_load_request.kwh_cost
        grid["emission_cost"] = deferred_load_request.co2_cost
        grid["emission_factor_sched"] = emission_factor_forecast
        system["grids"] = [grid]

        tssa = {}
        tssa["name"] = deferred_load_request.deferred_entity
        tssa["uid"] = 1
        tssa["bus_uid"] = 1
        tssa["load"] = deferred_load_request.load
        tssa["on_period"] = on_period
        system["tssas"] = [tssa]

        return system

    def get_emission_factor_forecast(self):
        """Get the emission factor forecast."""
        #
        # Get the forecasts
        #
        co2_entity = self.deferred_load_request.co2_intensity_entity

        # retrieve one day of history

        end_time = datetime.now().replace(microsecond=0)
        start_time = end_time - timedelta(
            hours=as_hours(self.deferred_load_request.time_horizont)
        )

        co2_intensity_history = self.ha_sqlconn.get_state_history(
            co2_entity,
            start_time=start_time,
            end_time=end_time,
            frequency=f"{self.dt}h",
        )

        emission_factor_history = co2_intensity_history[co2_entity].to_list()

        return emission_factor_history

    def get_tssa_system(self):
        """Get tssa system."""
        emission_factor_forecast = self.get_emission_factor_forecast()

        return DeferredLoad.create_tssa_system(
            deferred_load_request=self.deferred_load_request,
            emission_factor_forecast=emission_factor_forecast,
            block_duration=self.dt,
        )

    def get_on_delay(self):
        """Get start delay [seconds] for a deferred load."""
        #
        # create the system
        #

        system = self.get_tssa_system()
        if system is None:
            return timedelta(hours=0)

        #
        # Optimize the system remotely
        #
        headers = {"Content-Type": "application/json"}
        host = self.deferred_load_request.gilda_opts_host
        port = self.deferred_load_request.gilda_opts_port
        url = f"http://{host}:{port}/optimize"

        response = requests.post(url, headers=headers, json=system, timeout=100)
        if response.status_code == 200:
            system_sched = json.loads(response.content)
        else:
            return timedelta(hours=0)

        #
        # Calculate the delay
        #

        tssa_sched = system_sched["tssas"][0]

        delay = 0
        for onoff in tssa_sched["onoff_values"]:
            if float(onoff) != 0:
                break
            delay += self.dt

        return timedelta(hours=delay)


#  LocalWords:  durations
