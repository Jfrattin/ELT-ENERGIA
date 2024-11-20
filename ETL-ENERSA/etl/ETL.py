import pandas as pd
from sqlalchemy import create_engine
from dimension_utils import actualizarTablaDimension
from config import DB_CONNECTIONS

# Establecer conexiones a las bases de datos
engine_sf = create_engine(DB_CONNECTIONS["engine_sf"])
engine_cubo = create_engine(DB_CONNECTIONS["engine_cubo"])

# Lista de tablas y las columnas que necesito de cada una
tables = {
    "customers": ['customers_id', 'name', 'last_name'],
    "readings": ['readings_id', 'meter_id', 'consumption_kwh', 'reading_date'],
    "meters": ['meters_id', 'customer_id', 'installation_date'],
    "services": ['price'],
    "customeraddresses": ['customeraddresses_id', 'customer_id', 'city', 'street_name', 'street_number']
}

# Diccionario para almacenar cada DataFrame
dataframes = {}

# Conecta a la base de datos y extraer cada tabla
try:
    with engine_sf.connect() as conn:
        for table, columns in tables.items():
            # Construir la consulta SQL para seleccionar solo las columnas necesarias
            query = f"SELECT {', '.join(columns)} FROM {table}"
            dataframes[table] = pd.read_sql_query(query, conn)
except Exception as e:
    print(f"No se pudo conectar con la base de datos: {e}")

# Extraer cada tabla de los dataframes
customers = dataframes["customers"]
readings = dataframes["readings"]
meters = dataframes["meters"]
services = dataframes["services"]
customer_addresses = dataframes["customeraddresses"]

# -----------------------------------------------------------

# ----------------------------------------
# Crear la dimensión customers_d
# ----------------------------------------

# -----------------------------------------------------------

dimension_customers =pd.DataFrame({
    'first_name': customers['name'],
    'last_name': customers['last_name'],
    'customer_id': customers['customers_id']
})

dimension_customers = actualizarTablaDimension(engine_cubo, 'customers_d', dimension_customers, pk='customer_id')

print(dimension_customers)

# -----------------------------------------------------------

# ----------------------------------------
# Crear la dimensión meters_d
# ----------------------------------------

# -----------------------------------------------------------

dimension_meters = pd.DataFrame({
    'serial_number': meters['meters_id'],
    'installation_date': meters['installation_date']
})

dimension_meters = actualizarTablaDimension(engine_cubo, 'meters_d', dimension_meters, pk='serial_number')

print(dimension_meters)

# -----------------------------------------------------------

# ----------------------------------------
# Crear la dimensión geography_d
# ----------------------------------------

# -----------------------------------------------------------
dimension_geography = pd.DataFrame({
    'location_id': customer_addresses['customeraddresses_id'],
    'city': customer_addresses['city'],
    'street': customer_addresses['street_name'],
    'street_number': customer_addresses['street_number'].astype(str)
})


dimension_geography = actualizarTablaDimension(engine_cubo, 'geography_d', dimension_geography, pk='location_id')

print(dimension_geography)

# -----------------------------------------------------------

# ----------------------------------------
# Crear la dimensión time_d
# ----------------------------------------

# -----------------------------------------------------------
dimension_time = pd.DataFrame({
    'date': readings['reading_date'].unique()
})

# Desglosar la fecha en componentes adicionales si es necesario
dimension_time["year"] = dimension_time["date"].dt.year
dimension_time["month"] = dimension_time["date"].dt.month
dimension_time["day"] = dimension_time["date"].dt.day
dimension_time["hour"] = dimension_time["date"].dt.hour

#dimension_time.drop('date', axis=1, inplace=True)

dimension_time = actualizarTablaDimension(engine_cubo, 'time_d', dimension_time, pk='time_id')

print(dimension_time)


# -----------------------------------------------------------

# ----------------------------------------
# Tabla de Hechos electricity_consumption
# ----------------------------------------

# -----------------------------------------------------------

hechos_df = (
    readings
    .merge(meters, left_on='meter_id', right_on='meters_id')
    .merge(customers, left_on='customer_id', right_on='customers_id')
    .merge(customer_addresses, left_on='customers_id', right_on='customer_id')
)


# Asignar time_id en hechos_df usando map
hechos_df['time_id'] = hechos_df['reading_date'].map(dimension_time.set_index('date')['time_id'])

# Obtengo el precio por kWh
price_per_kwh = services['price'].iloc[0]  # O services['price'].values[0]

# Calculo el costo del consumo
hechos_df['consumption_cost'] = hechos_df['consumption_kwh'] * price_per_kwh

# Calculo el consumo promedio
hechos_df['average_consumption'] = hechos_df.groupby('customers_id')['consumption_kwh'].transform('mean')

# Creo el DataFrame directamente con kwargs
hechos_df = pd.DataFrame({
    # Dimensiones
    'customer_id': hechos_df['customers_id'],
    'serial_number': hechos_df['meters_id'],
    'location_id': hechos_df['customeraddresses_id'],
    'time_id': hechos_df['time_id'],

    # Métricas
    'consumption_kwh': hechos_df['consumption_kwh'],
    'average_consumption': hechos_df['average_consumption'],  # Valor escalar
    'consumption_cost': hechos_df['consumption_cost']
})


# Insertar los datos en la tabla de hechos
actualizarTablaDimension(engine_cubo, 'electricity_consumption_h', hechos_df, pk='electricity_consumption_id')

print(hechos_df)