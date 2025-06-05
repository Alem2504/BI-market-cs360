CREATE SCHEMA IF NOT EXISTS dwh_raw;

-- 1. STORES (SCD2)
CREATE TABLE IF NOT EXISTS dwh_raw.raw_stores (
    store_id INT,
    name VARCHAR(100),
    city VARCHAR(50),
    address VARCHAR(100),
    size VARCHAR(20),

    row_start_date TIMESTAMP NOT NULL,
    row_end_date TIMESTAMP NOT NULL DEFAULT '9999-12-31 00:00:00',
    update_id VARCHAR(50),

    PRIMARY KEY (store_id, row_start_date)
);

-- 2. PRODUCTS (SCD2)
CREATE TABLE IF NOT EXISTS dwh_raw.raw_products (
    product_id INT,
    name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    unit_price DECIMAL(10, 2),

    row_start_date TIMESTAMP NOT NULL,
    row_end_date TIMESTAMP NOT NULL DEFAULT '9999-12-31 00:00:00',
    update_id VARCHAR(50),

    PRIMARY KEY (product_id, row_start_date)
);

-- 3. CUSTOMERS (SCD2 optional)
CREATE TABLE IF NOT EXISTS dwh_raw.raw_customers (
    customer_id INT,
    gender VARCHAR(10),
    birth_year INT,
    city VARCHAR(50),

    row_start_date TIMESTAMP NOT NULL,
    row_end_date TIMESTAMP NOT NULL DEFAULT '9999-12-31 00:00:00',
    update_id VARCHAR(50),

    PRIMARY KEY (customer_id, row_start_date)
);

-- 4. CITY DEMOGRAPHICS (SCD2)
CREATE TABLE IF NOT EXISTS dwh_raw.raw_city_demographics (
    city VARCHAR(50),
    population INT,
    avg_age NUMERIC(5,2),
    employment_rate NUMERIC(4,2),
    avg_income_bam NUMERIC(10,2),
    edu_attainment_index NUMERIC(4,2),

    row_start_date TIMESTAMP NOT NULL,
    row_end_date TIMESTAMP NOT NULL DEFAULT '9999-12-31 00:00:00',
    update_id VARCHAR(50),

    PRIMARY KEY (city, row_start_date)
);

-- 5. TRANSACTIONS (NO SCD)
CREATE TABLE IF NOT EXISTS dwh_raw.raw_transactions (
    transaction_id INT,
    store_id INT,
    customer_id INT,
    transaction_date DATE,
    total_amount DECIMAL(10,2),
    update_id VARCHAR(50)
);

-- 6. SALES (NO SCD)
CREATE TABLE IF NOT EXISTS dwh_raw.raw_sales (
    sale_id INT,
    transaction_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2),
    update_id VARCHAR(50)
);

-- 7. PAYMENTS (NO SCD)
CREATE TABLE IF NOT EXISTS dwh_raw.raw_payments (
    payment_id INT,
    transaction_id INT,
    payment_method VARCHAR(50),
    amount_paid DECIMAL(10,2),
    update_id VARCHAR(50)
);
