from flask import Flask, render_template, request
import pandas as pd
from sqlalchemy import create_engine
import matplotlib
matplotlib.use('Agg')  # Configura matplotlib para entornos sin GUI
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from config import DB_CONNECTIONS

app = Flask(__name__)

# Conexión segura a la base de datos
engine = create_engine(DB_CONNECTIONS["engine_cubo"])


@app.route("/", methods=["GET", "POST"])
def index():
    query = """
    SELECT h.*, t.*, g.*, c.*
    FROM electricity_consumption_h h
    JOIN time_d t ON h.time_id = t.time_id
    JOIN geography_d g ON h.location_id = g.location_id
    JOIN customers_d c ON h.customer_id = c.customer_id
    """
    
    hechos_df = pd.read_sql(query, engine)

    cities = hechos_df['city'].unique()
    customers = hechos_df.apply(lambda x: f"{x['first_name']} {x['last_name']}", axis=1).unique()

    selected_city = request.form.get("city")
    selected_customer = request.form.get("customer")
    selected_scale = request.form.get("scale", "day")

    if selected_city:
        hechos_df = hechos_df[hechos_df['city'] == selected_city]
    
    if selected_customer:
        customer_name = selected_customer.split()
        hechos_df = hechos_df[(hechos_df['first_name'] == customer_name[0]) & (hechos_df['last_name'] == customer_name[1])]

    if selected_scale == "month":
        hechos_df["time_period"] = pd.to_datetime(hechos_df["date"]).dt.to_period("M")
    elif selected_scale == "quarter":
        hechos_df["time_period"] = pd.to_datetime(hechos_df["date"]).dt.to_period("Q")
    else:
        hechos_df["time_period"] = pd.to_datetime(hechos_df["date"]).dt.to_period("D")

    total_consumo = (
        hechos_df.groupby("time_period")[["consumption_kwh", "consumption_cost"]]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(total_consumo["time_period"].astype(str), total_consumo["consumption_kwh"], color='lightblue', label="Consumo Total (kWh)")
    ax.axhline(y=hechos_df["consumption_kwh"].mean(), color='salmon', linestyle="--", label="Consumo Promedio (kWh)")
    ax.set_title("Consumo de Energía en kWh")
    ax.set_xlabel(f"Tiempo ({selected_scale.capitalize()})")
    ax.set_ylabel("Consumo (kWh)")
    ax.legend()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_consumption = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(total_consumo["time_period"].astype(str), total_consumo["consumption_cost"], color='lightcoral', label="Costo Total ($)")
    ax.set_title("Costo de Consumo en el Tiempo")
    ax.set_xlabel(f"Tiempo ({selected_scale.capitalize()})")
    ax.set_ylabel("Costo ($)")
    ax.legend()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_cost = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close(fig)

    return render_template(
        "index.html",
        cities=cities,
        customers=customers,
        image_consumption=image_consumption,
        image_cost=image_cost,
        selected_city=selected_city,
        selected_customer=selected_customer,
        selected_scale=selected_scale
    )

@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    # Capturar los filtros seleccionados
    selected_customer = request.form.get("customer")
    selected_scale = request.form.get("scale", "day")
    
    # Si se seleccionó un cliente, ejecutar una consulta específica para ese cliente
    if selected_customer:
        # Dividir el nombre del cliente en first_name y last_name
        customer_name_parts = selected_customer.split()
        
        if len(customer_name_parts) == 2:  # Asegurarse de que tenga nombre y apellido
            first_name, last_name = customer_name_parts
            query = """
            SELECT *
            FROM electricity_consumption_h h
            JOIN time_d t ON h.time_id = t.time_id
            JOIN geography_d g ON h.location_id = g.location_id
            JOIN customers_d c ON h.customer_id = c.customer_id
            WHERE c.first_name LIKE %(first_name)s AND c.last_name LIKE %(last_name)s
            """
            params = {"first_name": f"%{first_name}%", "last_name": f"%{last_name}%"}

        else:
            # Si el nombre no está en el formato esperado, usar una consulta general
            query = """
            SELECT *
            FROM electricity_consumption_h h
            JOIN time_d t ON h.time_id = t.time_id
            JOIN geography_d g ON h.location_id = g.location_id
            JOIN customers_d c ON h.customer_id = c.customer_id
            """
            params = {}  # No hay parámetros adicionales
    else:
        # Si no se seleccionó ningún cliente, cargar todos los datos
        query = """
        SELECT *
        FROM electricity_consumption_h h
        JOIN time_d t ON h.time_id = t.time_id
        JOIN geography_d g ON h.location_id = g.location_id
        JOIN customers_d c ON h.customer_id = c.customer_id
        """
        params = {}  # No hay parámetros adicionales
    
    # Ejecutar la consulta y cargar los datos en un DataFrame
    hechos_df = pd.read_sql(query, engine, params=params)
    
    # Obtener lista de clientes (nombre completo) para el menú desplegable
    customers = hechos_df.apply(lambda x: f"{x['first_name']} {x['last_name']}", axis=1).unique()

    # Ajustar la escala de tiempo
    if selected_scale == "month":
        hechos_df["time_period"] = pd.to_datetime(hechos_df["date"]).dt.to_period("M")
    elif selected_scale == "quarter":
        hechos_df["time_period"] = pd.to_datetime(hechos_df["date"]).dt.to_period("Q")
    else:
        hechos_df["time_period"] = pd.to_datetime(hechos_df["date"]).dt.to_period("D")

    # Agrupar y calcular totales
    total_consumo = (
        hechos_df.groupby("time_period")[["consumption_kwh", "consumption_cost"]]
        .sum()
        .reset_index()
    )

    # Gráfico de Consumo
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(total_consumo["time_period"].astype(str), total_consumo["consumption_kwh"], color='lightblue', label="Consumo Total (kWh)")
    ax.axhline(y=hechos_df["consumption_kwh"].mean(), color='salmon', linestyle="--", label="Consumo Promedio (kWh)")
    ax.set_title(f"Consumo de Energía en kWh para {selected_customer or 'todos los clientes'}")
    ax.set_xlabel(f"Tiempo ({selected_scale.capitalize()})")
    ax.set_ylabel("Consumo (kWh)")
    ax.legend()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_consumption = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close(fig)

    # Gráfico de Costo
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(total_consumo["time_period"].astype(str), total_consumo["consumption_cost"], color='lightcoral', label="Costo Total ($)")
    ax.set_title(f"Costo de Consumo en el Tiempo para {selected_customer or 'todos los clientes'}")
    ax.set_xlabel(f"Tiempo ({selected_scale.capitalize()})")
    ax.set_ylabel("Costo ($)")
    ax.legend()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_cost = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close(fig)

    return render_template(
        "clientes.html",
        customers=customers,
        image_consumption=image_consumption,
        image_cost=image_cost,
        selected_customer=selected_customer,
        selected_scale=selected_scale
    )

if __name__ == "__main__":
    app.run(debug=True)
