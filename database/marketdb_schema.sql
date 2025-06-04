-- 1. PRODUCTS
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    brand VARCHAR(50),
    unit_price DECIMAL(10, 2) NOT NULL
);

-- 2. STORES
CREATE TABLE stores (
    store_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    address VARCHAR(100),
    size VARCHAR(20)  -- Mali, Srednji, Veliki
);

-- 3. CUSTOMERS (opciono, korisno za analizu po kupcima)
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    gender VARCHAR(10),         -- M / Ž
    birth_year INT,
    city VARCHAR(50)
);

-- 4. TRANSACTIONS (računi – zaglavlja)
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    store_id INT REFERENCES stores(store_id),
    customer_id INT REFERENCES customers(customer_id),
    transaction_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL
);

-- 5. SALES (stavke na računu – po proizvodu)
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    transaction_id INT REFERENCES transactions(transaction_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL
);

-- 6. PAYMENTS (način plaćanja po računu)
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    transaction_id INT UNIQUE REFERENCES transactions(transaction_id),
    payment_method VARCHAR(50) NOT NULL,  -- Gotovina, Kartica, Mobilno, Bon
    amount_paid DECIMAL(10,2) NOT NULL
);
