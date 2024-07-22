"""ElectricCar module represents an Electric Car."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.bess import Battery
from gilda_opts.utils import IntSched, NumberSched


def default_battery():
    """Return the default battery for an electric_car."""
    return Battery(
        capacity=50,
        max_flow_in=50,
        max_flow_out=0,
        efficiency_in=0.95,
        efficiency_out=0.95,
        emin_profile_sched=0.2,
        emax_profile_sched=0.9,
    )


@dataclass
class Engine(BaseClassJson):
    """
    Engine represetns an Electric Engine.

    Attributes:
    -----------
    energy_efficiency:   Energy efficiency [Km/Kwh]
    """

    energy_efficiency: float = 8.0


@dataclass
class ElectricCar(BaseClassJson):
    """
    ElectricCar represents an Electric Car.

    Attributes:
    -----------
    uid:                    ElectricCar unique id
    name:                   ElectricCar name
    athome_bus_uid:         Bus uid to be connected to at home
    charger_bus_uid:        Bus uid to be connected to on public charger

    battery:                Storage system [Battery]
    engine:                 Electric engine [Engine]

    bus_uid_sched:          Bus_id where is plugged or unplugged=-1
    distance_sched:         Traveled distances while on road [Km]

    cfail_sched:            Fail distance cost, you may use the taxi tariff [$/Km]

    """

    uid: int = -1
    name: str = ""

    battery: Battery = field(default_factory=default_battery)
    engine: Engine = field(default_factory=Engine)

    bus_uid_sched: IntSched = -1
    distance_sched: NumberSched = 0
    cfail_sched: NumberSched = -1
