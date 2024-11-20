-- Insertar datos de clientes
INSERT INTO customers (
    name,
    last_name,
    dni,
    phone_number,
    email,
    account_number
)
VALUES
    ('Juan', 'Pérez', '25898123', '555-1234', 'juan.perez@example.com', 'ACC123456'),
    ('María', 'Gómez', '3955777', '555-5678', 'maria.gomez@example.com', 'ACC654321'),
    ('Carlos', 'López', '7568777', '555-8765', 'carlos.lopez@example.com', 'ACC789012');

-- Insertar direcciones para cada cliente
INSERT INTO customeraddresses (
    customer_id,
    city,
    street_name,
    street_number
)
VALUES
    ((SELECT customers_id FROM customers WHERE account_number = 'ACC123456'), 'Paraná', 'Av. Ramirez', 1234),
    ((SELECT customers_id FROM customers WHERE account_number = 'ACC654321'), 'Paraná', 'Calle Urquiza', 5678),
    ((SELECT customers_id FROM customers WHERE account_number = 'ACC789012'), 'Paraná', 'Bv. Racedo', 4321);

-- Insertar 1 medidor para cada cliente
INSERT INTO meters (
    customer_id,
    installation_date,
    meter_type,
    latitude,
    longitude,
    city,
    street_name,
    street_number
)
VALUES
    (
        (SELECT customers_id FROM customers WHERE account_number = 'ACC123456'),
        '2023-01-01',
        'Smart',
        -31.736891,
        -60.540012,
        'Paraná',
        'Av. Ramirez',
        1234
    ),
    (
        (SELECT customers_id FROM customers WHERE account_number = 'ACC654321'),
        '2023-01-02',
        'Smart',
        -31.736891,
        -60.540012,
        'Paraná',
        'Calle Urquiza',
        5678
    ),
    (
        (SELECT customers_id FROM customers WHERE account_number = 'ACC789012'),
        '2023-01-03',
        'Smart',
        -31.736891,
        -60.540012,
        'Paraná',
        'Bv. Racedo',
        4321
    );

-- Insertar lecturas de consumo por hora para cada medidor
INSERT INTO readings (
    meter_id,
    reading_date,
    consumption_kwh,
    billing_cycle
)
SELECT 
    m.meters_id,
    gs.reading_date,
    ROUND((RANDOM() * 0.8 + 0.1)::NUMERIC, 2) AS consumption_kwh,
    TO_CHAR(gs.reading_date, 'YYYY-MM') AS billing_cycle
FROM 
    meters m,
    GENERATE_SERIES(
        '2023-01-01 00:00'::TIMESTAMP, 
        '2023-03-12 23:00'::TIMESTAMP, 
        '1 hour'
    ) AS gs(reading_date);

-- Insertar datos de servicios
INSERT INTO services (
    name,
    description,
    price
)
VALUES
    ('Domiciliario', 'Servicio de suministro de electricidad para hogares', 150.00);

-- Insertar datos de suscripciones
INSERT INTO subscriptions (
    customers_id,
    service_id,
    start_date,
    status
)
VALUES
    (
        (SELECT customers_id FROM customers WHERE account_number = 'ACC123456'),
        (SELECT services_id FROM services WHERE name = 'Domiciliario'),
        '2023-01-01',
        'activa'
    ),
    (
        (SELECT customers_id FROM customers WHERE account_number = 'ACC654321'),
        (SELECT services_id FROM services WHERE name = 'Domiciliario'),
        '2023-01-02',
        'activa'
    ),
    (
        (SELECT customers_id FROM customers WHERE account_number = 'ACC789012'),
        (SELECT services_id FROM services WHERE name = 'Domiciliario'),
        '2023-01-03',
        'activa'
    );