-- Tabla de Clientes
CREATE TABLE customers (
    customers_id SERIAL PRIMARY KEY,
    name CHAR (20) NOT NULL,
    last_name CHAR (20) NOT NULL,
	dni bigint NOT NULL,
    phone_number CHAR (20),
    email CHAR (30),
    account_number text UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Direcciones de Clientes (direcciones secundarias)
CREATE TABLE customeraddresses (
    customeraddresses_id SERIAL PRIMARY KEY,
    customer_id SERIAL NOT NULL REFERENCES customers(customers_id) ON DELETE CASCADE,
    city VARCHAR(20) NOT NULL,
    street_name VARCHAR(50) NOT NULL,
    street_number INT NOT NULL
);

-- Tabla de Medidores
CREATE TABLE meters (
    meters_id SERIAL PRIMARY KEY,
    customer_id SERIAL NOT NULL REFERENCES customers(customers_id) ON DELETE CASCADE,
    installation_date TIMESTAMP NOT NULL,
    meter_type CHAR (20) NOT NULL,
    status CHAR (20) DEFAULT 'activo',
    last_maintenance_date DATE,
	latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    city VARCHAR(20) NOT NULL,
    street_name VARCHAR(50) NOT NULL,
    street_number INT NOT NULL
);

-- Tabla de Lecturas de Consumo
CREATE TABLE readings (
    readings_id SERIAL PRIMARY KEY,
    meter_id SERIAL NOT NULL REFERENCES meters(meters_id) ON DELETE CASCADE,
    reading_date TIMESTAMP NOT NULL,
    consumption_kwh DECIMAL(10, 2) NOT NULL,
    billing_cycle CHAR (20),
    is_estimated BOOLEAN DEFAULT FALSE
);

-- Tabla de Servicios
CREATE TABLE services (
    services_id SERIAL PRIMARY KEY,
    name CHAR (20) NOT NULL,
    description text,
    price DECIMAL(10, 2) NOT NULL
);

-- Tabla de Suscripciones
CREATE TABLE subscriptions (
    subscriptions_id SERIAL PRIMARY KEY,
    customers_id SERIAL NOT NULL REFERENCES customers(customers_id) ON DELETE CASCADE,
    service_id SERIAL NOT NULL REFERENCES services(services_id) ON DELETE CASCADE,
    start_date TIMESTAMP NOT NULL,
    status CHAR (20) DEFAULT 'activa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancellation_date DATE
);

-- Tabla de Facturas
CREATE TABLE bills (
    bill_id SERIAL PRIMARY KEY,  -- ID único para la factura
    customer_name CHAR(100) NOT NULL,  -- Nombre del titular o razón social
    postal_address CHAR(150) NOT NULL,  -- Domicilio postal
    link_code CHAR(50) NOT NULL UNIQUE,  -- Código LINK para pago en cajeros automáticos/Home Banking
    service_id INT NOT NULL REFERENCES services(services_id) ON DELETE CASCADE,  -- FK de servicio
    supply_address CHAR(150) NOT NULL,  -- Domicilio donde se brinda el suministro
    reading_start_date DATE NOT NULL,  -- Fecha de inicio de lectura
    reading_end_date DATE NOT NULL,  -- Fecha de fin de lectura
    meter_id INT NOT NULL REFERENCES meters(meters_id) ON DELETE CASCADE,  -- FK de medidor
    due_date DATE NOT NULL,  -- Fecha de vencimiento de la factura
    total_amount DECIMAL(10, 2) NOT NULL,  -- Total de la factura
    bill_line INT NOT NULL,  -- Renglón o número de línea de la factura
    first_due_date DATE NOT NULL,  -- Fecha de vencimiento de la primera cuota
    second_due_date DATE,  -- Fecha de vencimiento de la segunda cuota
    suspension_date DATE,  -- Fecha en la que ENERSA puede suspender el suministro
    created_at DATE DEFAULT CURRENT_TIMESTAMP  -- Fecha de creación de la factura
);
