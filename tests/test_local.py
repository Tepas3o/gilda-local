"""Tests for gilda-local."""

# import os
# from datetime import datetime, timedelta
# from homeassistant_api import Client
# import numpy as np


def to_float(s):
    """Convert to float."""
    try:
        return float(s)
    except Exception:  # pylint: disable=W0718
        return float("nan")


def test_local():
    """Test local."""
    assert to_float("1.5") == 1.5


# def test_local_1():
#     # Configuración de la conexión a la base de datos
#     # mysql://homeassistant:password@core-mariadb/homeassistant?charset=utf8mb4
#     config = {
#         'user': 'homeassistant',  # Reemplaza con tu usuario de MariaDB
#         'password': 'elperro123',  # Reemplaza con tu contraseña de MariaDB
#         'host': '192.168.1.85',  # Reemplaza con la dirección de tu host si es diferente
#         'database': 'homeassistant',  # Reemplaza con el nombre de tu base de datos
#     }
#     # Crear conexión
#     conn = mariadb.connect(
#         user="homeassistant",
#         password="elperro123",
#         host="192.168.1.85",
#         port=3306,
#         database="homeassistant"

#     )
#     # conn = mysql.connector.connect(**config)
#     # Crear un cursor para ejecutar la consulta
#     cursor = conn.cursor()
#     # Consulta SQL
#     query = """
#     SELECT from_unixtime(last_updated_ts), state
#     FROM states
#     INNER JOIN states_meta ON states.metadata_id = states_meta.metadata_id
#     WHERE states_meta.entity_id = 'sensor.electricity_maps_co2_intensity'
#     ORDER BY last_updated_ts
#     """

#     # Ejecutar la consulta
#     cursor.execute(query)

#     # Obtener el resultado
#     for result in cursor:
#         # Imprimir el resultado
#         if result:
#             print("Estado:", result[0], result[1])
#         else:
#             print("No se encontró ningún resultado.")


#     assert False


# def test_local_2():
#     api_url = "http://192.168.1.85:8123/api"  # Something like http://localhost:8123/api
#     token = os.getenv(
#         "HOMEASSISTANT_TOKEN"
#     )  # Used to aunthenticate yourself with homeassistant
#     # See the documentation on how to obtain a Long Lived Access Token

#     token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2NGZlZjIzYTAzNmQ0YTJhOGI2NDNmYzY3MTU2OGMyNyIsImlhdCI6MTcyMjQwMzc2MCwiZXhwIjoyMDM3NzYzNzYwfQ.PF--9gieQrCSrA150E58hvZiYNUcIKA3NVf9o76UF40" # pylint: disable=C0301

#     assert token is not None

#     with Client(
#             api_url,
#             token,
#     ) as client:  # Create Client object and check that its running.
#         entities = client.get_entities()
#         for s, g in entities.items():
#             for n, e in g.entities.items():
#                 print("entity", s, n, e.slug)

#         sensor = client.get_entity(entity_id="sensor.gilda_co2_intensity")

#         # Tells Home Assistant to trigger the toggle service on the given entity_id
#         co2_state = sensor.get_state()

#         print("state", co2_state.state)

#         # Timestamp de hoy
#         timestamp_hoy = datetime.now()
#         print("Timestamp de hoy:", timestamp_hoy)

#         # Calcular la fecha de un mes atrás
#         un_mes_atras = timestamp_hoy - timedelta(days=30)
#         print("Timestamp de un mes atrás:", un_mes_atras)

#         sensor_history = client.get_entity_histories(
#             entities=[sensor],
#             start_timestamp=un_mes_atras,
#             end_timestamp=timestamp_hoy,
#         )

#         # Tells Home Assistant to trigger the toggle service on the given entity_id
#         for co2_state in sensor_history:
#             values = [ (s.last_updated, to_float(s.state)) for s in co2_state.states ]
#             df = np.array(values)
#             print("df", df)

#         assert False
