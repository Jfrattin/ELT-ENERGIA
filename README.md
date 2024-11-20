Proyecto: Medidor Eléctrico Inteligente IoT
Este proyecto fue desarrollado como parte de la materia Bases de Datos Multidimensionales, y consistió en diseñar y gestionar los datos generados por un medidor eléctrico inteligente con capacidades de Internet de las Cosas (IoT).

Descripción
El objetivo principal fue proponer una solución integral para el manejo y procesamiento de los datos generados por el dispositivo, enfocándonos en:

Diseño de bases de datos multidimensionales.
Implementación de procesos de gestión y análisis de datos.
Desarrollo de una API para interactuar con los datos en tiempo real.
Herramientas Utilizadas
PostgreSQL: Para la gestión de la base de datos relacional.
SQLAlchemy: Como ORM para interactuar con la base de datos.
Python y Flask: Para el desarrollo de una API que permite la consulta y manipulación de los datos del medidor eléctrico.
Funcionalidades
Gestión de datos de consumo energético en tiempo real.
Consulta de datos históricos mediante endpoints de la API.
Diseño de un modelo de datos optimizado para análisis y visualización futura.
Este repositorio contiene:

El esquema de la base de datos en PostgreSQL.
Los scripts para configurar y poblar la base de datos.
La implementación de la API desarrollada en Flask.
Cómo Ejecutar
Clona este repositorio en tu máquina local.
Configura una instancia de PostgreSQL y ejecuta los scripts de creación de la base de datos.
Instala las dependencias de Python listadas en requirements.txt.
Inicia la API con:
bash
Copiar código
python app.py  
Accede a los endpoints disponibles para interactuar con los datos.
Futuras Mejoras
Incorporación de análisis predictivo con algoritmos de inteligencia artificial.
Visualización de datos en dashboards interactivos.
Integración con servicios de nube para escalabilidad.
