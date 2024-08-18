"""Request module contains the mechanism to request information from HA."""

from datetime import datetime, timedelta

import mariadb
import pandas as pd

from gilda_local.sql_config import SQLConfig


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
        end_time: datetime | None = None,
        frequency: str | None = "1h",
    ):
        """Get the state history for a given entity.

        entity_id: entity name, such as 'sensor.electricity_maps_co2_intensity'.
        """
        # Crear un cursor para ejecutar la consulta
        cursor = self.conn.cursor()
        # Consulta SQL

        end_time_ts = (
            end_time.timestamp()
            if end_time is not None
            else datetime.now().replace(microsecond=0).timestamp()
        )
        start_time_ts = (
            start_time.timestamp()
            if start_time is not None
            else end_time_ts - (24 * 3600)
        )

        start_time = datetime.fromtimestamp(start_time_ts)
        end_time = datetime.fromtimestamp(end_time_ts)

        if frequency:
            end_time_ts += 2 * 3600
            start_time_ts -= 2 * 3600

        query = f"""
        SELECT last_updated_ts, state
        FROM states
        INNER JOIN states_meta ON states.metadata_id = states_meta.metadata_id
        WHERE states_meta.entity_id = '{entity_id}'
        AND last_updated_ts BETWEEN {start_time_ts} AND {end_time_ts}
        ORDER BY last_updated_ts
        """

        cursor.execute(query)

        # get the raw data
        ts_col = []
        state_col = []
        for ts, state in cursor:
            try:
                date_hour = datetime.fromtimestamp(float(ts))
                value = float(state)

                ts_col.append(date_hour)
                state_col.append(value)
            except Exception:  # pylint: disable=W0718
                pass

        df = pd.DataFrame({"timestamp": ts_col, entity_id: state_col})
        df.set_index("timestamp", inplace=True)

        # remove the duplicate timestamps
        df = df[~df.index.duplicated(keep="last")]

        # fill the gaps
        if frequency:
            desired_index = pd.date_range(
                start=start_time, end=end_time, freq=frequency
            )
            df = (
                df.reindex(df.index.union(desired_index))
                .interpolate(method="time")
                .reindex(desired_index)
                .sort_index()
            )

        return df.dropna()

    def get_state_histories(
        self,
        entity_ids: list[str],
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        frequency: str | None = "1h",
    ):
        """Get the state history for a given entities.

        entity_ids: list of entity names.
        """

        end_time = (
            end_time if end_time is not None else datetime.now().replace(microsecond=0)
        )
        start_time = (
            start_time if start_time is not None else end_time - timedelta(hours=24)
        )

        if len(entity_ids) == 0:
            return None

        df = self.get_state_history(entity_ids[0], start_time, end_time, frequency)
        for entity_id in entity_ids[1:]:
            df_e = self.get_state_history(
                entity_id, start_time, end_time, frequency
            )
            df = pd.merge(df, df_e, left_index=True, right_index=True, how="outer")

        return df
