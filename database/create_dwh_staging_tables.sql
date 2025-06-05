CREATE SCHEMA IF NOT EXISTS dwh_stg;

-- PRODUCTS
CREATE TABLE IF NOT EXISTS dwh_stg.stg_products (
    product_id INT,
    name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    unit_price DECIMAL(10, 2)
);

-- STORES
CREATE TABLE IF NOT EXISTS dwh_stg.stg_stores (
    store_id INT,
    name VARCHAR(100),
    city VARCHAR(50),
    address VARCHAR(100),
    size VARCHAR(20)
);

-- CUSTOMERS
CREATE TABLE IF NOT EXISTS dwh_stg.stg_customers (
    customer_id INT,
    gender VARCHAR(10),
    birth_year INT,
    city VARCHAR(50)
);

-- TRANSACTIONS
CREATE TABLE IF NOT EXISTS dwh_stg.stg_transactions (
    transaction_id INT,
    store_id INT,
    customer_id INT,
    transaction_date DATE,
    total_amount DECIMAL(10,2)
);

-- SALES
CREATE TABLE IF NOT EXISTS dwh_stg.stg_sales (
    sale_id INT,
    transaction_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2)
);

-- PAYMENTS
CREATE TABLE IF NOT EXISTS dwh_stg.stg_payments (
    payment_id INT,
    transaction_id INT,
    payment_method VARCHAR(50),
    amount_paid DECIMAL(10,2)
);

-- CITY DEMOGRAPHICS (CSV izvor)
CREATE TABLE IF NOT EXISTS dwh_stg.stg_city_demographics (
    city VARCHAR(50),
    population INT,
    avg_age NUMERIC(5,2),
    employment_rate NUMERIC(4,2),
    avg_income_bam NUMERIC(10,2),
    edu_attainment_index NUMERIC(4,2)
);
