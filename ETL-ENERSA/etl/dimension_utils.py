import pandas as pd

def actualizarTablaDimension(engine, table, data, pk="id"):
    """
    Esta función actualiza una tabla de dimensión de un DW con los datos nuevos. Si los datos
    ya existen en la tabla, no se agregan. Devuelve la tabla actualizada con los pk tal cual está
    en la base de datos.

    La tabla de dimensión debe estar creada y las columnas deben llamarse igual que en el df.

    Parámetros:
        engine: engine de la base de datos
        table: nombre de la tabla
        data: DataFrame de datos nuevos a agregar, sin incluir la PK
        pk: nombre de la PK. Por defecto es "ID"

    Retorno:
        dimension_df: DataFrame con la tabla según está en la DB con los datos nuevos agregados.

    """
    with engine.connect() as conn:
        # Leer la tabla actual desde la base de datos
        old_data = pd.read_sql_table(table, conn)

        # Quitar la columna PK para comparar solo los datos
        old_data_nopk = old_data.drop(columns=[pk])

        # Filtrar los nuevos datos que no estén en la tabla
        new_data = data.merge(old_data_nopk, how='outer', indicator=True).query('_merge == "left_only"').drop(columns='_merge')

        # Insertar los nuevos datos
        if not new_data.empty:
            new_data.to_sql(table, conn, if_exists='append', index=False)

        # Obtener la tabla actualizada
        dimension_df = pd.read_sql_table(table, conn)

    return dimension_df
