"""Tests for gilda-local."""

from gilda_local.ha_sqlconn import HASQLConn, SQLConfig


def test_local():
    """Test local."""

    config = SQLConfig(
        user="homeassistant",
        password="elperro123",
        host="192.168.1.85",
    )

    conn = HASQLConn(config)

    sh = conn.get_state_histories(
        [
            "sensor.electricity_maps_co2_intensity",
            "sensor.electricity_maps_co2_intensity",
        ]
    )

    assert len(sh) == 24
