CREATE TABLE meters_d (
  serial_number SERIAL PRIMARY KEY,
  installation_date DATE NOT NULL
);

CREATE TABLE customers_d (
  customer_id SERIAL PRIMARY KEY,
  first_name VARCHAR(30) NOT NULL,
  last_name VARCHAR(30) NOT NULL
);

CREATE TABLE geography_d (
  location_id SERIAL PRIMARY KEY,
  city VARCHAR(30) NOT NULL,
  street VARCHAR(30) NOT NULL,
  street_number VARCHAR(30) NOT NULL
);

CREATE TABLE time_d (
  time_id SERIAL PRIMARY KEY,
  date TIMESTAMP NOT NULL,
  year INT NOT NULL,
  month INT NOT NULL,
  day INT NOT NULL,
  hour INT NOT NULL
);

CREATE TABLE electricity_consumption_h (
  electricity_consumption_id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers_d (customer_id),
  serial_number INT REFERENCES meters_d (serial_number),
  location_id INT REFERENCES geography_d (location_id),
  time_id INT REFERENCES time_d (time_id),
  consumption_kwh REAL,
  average_consumption REAL,
  consumption_cost REAL
);