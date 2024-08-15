"""Request module contains the mechanism to request information from HA."""

from datetime import datetime, timedelta

import mariadb
import pandas as pd

from pydantic import BaseModel


class SQLConfig(BaseModel):
    """SQL Config to establish the connection."""
    user: str = "homeassistant"
    password: str
    host: str = "homeassistant.local"
    database: str = "homeassistant"
    port: int = 3306


class HASQLConn:
    """Homeassistant SQL Connection class."""

    def __init__(self, config: SQLConfig):
        """Initialize the connection."""
        # Create connection
        self.conn = mariadb.connect(
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
            database=config.database,
        )

    def get_state_history(
        self,
        entity_id: str,
        start_time: datetime | None = None,
        stop_time: datetime | None = None,
        interpolation_method: str | None = None,
    ):
        """Get the state history for a given entity.

        entity_id: entity name, such as 'sensor.electricity_maps_co2_intensity'.
        """
        # Crear un cursor para ejecutar la consulta
        cursor = self.conn.cursor()
        # Consulta SQL

        stop_time_ts = (
            stop_time.timestamp()
            if stop_time is not None
            else datetime.now().timestamp()
        ) + 2
        start_time_ts = (
            start_time.timestamp()
            if start_time is not None
            else stop_time_ts - (24 * 60 * 60) - 2
        ) - 2

        query = f"""
        SELECT last_updated_ts, state
        FROM states
        INNER JOIN states_meta ON states.metadata_id = states_meta.metadata_id
        WHERE states_meta.entity_id = '{entity_id}'
        AND last_updated_ts BETWEEN {start_time_ts} AND {stop_time_ts}
        ORDER BY last_updated_ts
        """

        # Ejecutar la consulta
        cursor.execute(query)

        # Obtener el resultado
        ts_col = []
        state_col = []
        for ts, state in cursor:
            try:
                date_hour = datetime.fromtimestamp(float(ts)).replace(
                    minute=0, second=0, microsecond=0
                )
                value = float(state)

                ts_col.append(date_hour)
                state_col.append(value)
            except Exception:  # pylint: disable=W0718
                pass

        data = {"timestamp": ts_col, entity_id: state_col}

        df = pd.DataFrame(data)

        df.set_index("timestamp", inplace=True)

        # remove the duplicate timestamps
        df = df[~df.index.duplicated(keep="last")]

        # fill the gaps
        if interpolation_method:
            df = df.interpolate(method=interpolation_method)

        return df

    def get_state_histories(
        self,
        entity_ids: list[str],
        start_time: datetime | None = None,
        stop_time: datetime | None = None,
        interpolation_method: str | None = None,
    ):
        """Get the state history for a given entities.

        entity_ids: list of entity names.

        """
        if len(entity_ids) == 0:
            return None

        stop_time = stop_time if stop_time is not None else datetime.now()
        start_time = (
            start_time if start_time is not None else stop_time - timedelta(hours=24)
        )

        df = self.get_state_history(
            entity_ids[0], start_time, stop_time, interpolation_method
        )
        if len(entity_ids) > 1:
            for entity_id in entity_ids[1:]:
                df_e = self.get_state_history(
                    entity_id, start_time, stop_time, interpolation_method
                )
                df = pd.merge(df, df_e, left_index=True, right_index=True, how="outer")

        if interpolation_method:
            df = df.interpolate(method=interpolation_method)

        return df


if __name__ == "__main__":
    sql_config = SQLConfig(user="homeassistant", password="elperro123", host="192.168.1.85")
    conn = HASQLConn(sql_config)

    sh = conn.get_state_histories(
        [
            "sensor.electricity_maps_co2_intensity",
            "sensor.electricity_maps_co2_intensity",
        ]
    )
