CREATE SCHEMA IF NOT EXISTS dwh_star;

-- 1. DIM_PRODUCT (SCD2)
CREATE TABLE dwh_star.dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    unit_price DECIMAL(10, 2),
    effective_from TIMESTAMP NOT NULL,
    effective_to TIMESTAMP NOT NULL DEFAULT '9999-12-31 23:59:59',
    UNIQUE(product_id, effective_from)
);

-- 2. DIM_STORE (SCD2)
CREATE TABLE dwh_star.dim_store (
    store_key SERIAL PRIMARY KEY,
    store_id INT NOT NULL,
    name VARCHAR(100),
    city VARCHAR(50),
    address VARCHAR(100),
    size VARCHAR(20),
    city_key INT,
    effective_from TIMESTAMP NOT NULL,
    effective_to TIMESTAMP NOT NULL DEFAULT '9999-12-31 23:59:59',
    UNIQUE(store_id, effective_from)
);

-- 3. DIM_CUSTOMER (SCD2)
CREATE TABLE dwh_star.dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    gender VARCHAR(10),
    birth_year INT,
    city VARCHAR(50),
    city_key INT,
    effective_from TIMESTAMP NOT NULL,
    effective_to TIMESTAMP NOT NULL DEFAULT '9999-12-31 23:59:59',
    UNIQUE(customer_id, effective_from)
);

-- 4. DIM_CITY_DEMOGRAPHICS (SCD2)
CREATE TABLE dwh_star.dim_city_demographics (
    city_key SERIAL PRIMARY KEY,
    city VARCHAR(50) UNIQUE NOT NULL,
    population INT,
    avg_age NUMERIC(5,2),
    employment_rate NUMERIC(4,2),
    avg_income_bam NUMERIC(10,2),
    edu_attainment_index NUMERIC(4,2),
    effective_from TIMESTAMP NOT NULL,
    effective_to TIMESTAMP NOT NULL DEFAULT '9999-12-31 23:59:59'
);

-- 5. DIM_DATE (staticka dimenzija)
CREATE TABLE dwh_star.dim_date (
    date_key SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    day INT,
    month INT,
    year INT,
    quarter INT,
    weekday INT
);

-- 6. FACT_SALES
CREATE TABLE dwh_star.fact_sales (
    fact_key SERIAL PRIMARY KEY,
    product_key INT REFERENCES dwh_star.dim_product(product_key),
    store_key INT REFERENCES dwh_star.dim_store(store_key),
    customer_key INT REFERENCES dwh_star.dim_customer(customer_key),
    date_key INT REFERENCES dwh_star.dim_date(date_key),
    quantity INT,
    total_price DECIMAL(10, 2)
);
