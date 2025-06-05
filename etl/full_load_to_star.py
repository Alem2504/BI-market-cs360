import psycopg2

def full_load_dwh_star():
    conn = psycopg2.connect(
        dbname="market_dwh",
        user="postgres",
        password="Alem",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # 1. Dim_product (bez effective_from, effective_to)
    cur.execute("TRUNCATE TABLE dwh_star.dim_product CASCADE;")
    cur.execute("""
        INSERT INTO dwh_star.dim_product (product_id, name, category, brand, unit_price)
        SELECT product_id, name, category, brand, unit_price
        FROM dwh_raw.raw_products
        WHERE row_end_date = '9999-12-31 00:00:00';
    """)

    # 2. Dim_store
    cur.execute("TRUNCATE TABLE dwh_star.dim_store CASCADE;")
    cur.execute("""
        INSERT INTO dwh_star.dim_store (store_id, name, city, address, size, city_key)
        SELECT store_id, name, city, address, size, NULL  -- city_key možeš postaviti naknadno ako želiš
        FROM dwh_raw.raw_stores
        WHERE row_end_date = '9999-12-31 00:00:00';
    """)

    # 3. Dim_customer
    cur.execute("TRUNCATE TABLE dwh_star.dim_customer CASCADE;")
    cur.execute("""
        INSERT INTO dwh_star.dim_customer (customer_id, gender, birth_year, city, city_key)
        SELECT customer_id, gender, birth_year, city, NULL
        FROM dwh_raw.raw_customers
        WHERE row_end_date = '9999-12-31 00:00:00';
    """)

    # 4. Dim_city_demographics
    cur.execute("TRUNCATE TABLE dwh_star.dim_city_demographics CASCADE;")
    cur.execute("""
        INSERT INTO dwh_star.dim_city_demographics (city, population, avg_age, employment_rate, avg_income_bam, edu_attainment_index)
        SELECT city, population, avg_age, employment_rate, avg_income_bam, edu_attainment_index
        FROM dwh_raw.raw_city_demographics
        WHERE row_end_date = '9999-12-31 00:00:00';
    """)

    # 5. Dim_date
    cur.execute("TRUNCATE TABLE dwh_star.dim_date CASCADE;")
    cur.execute("""
        INSERT INTO dwh_star.dim_date (date, day, month, year, quarter, weekday)
        SELECT DISTINCT 
            transaction_date,
            EXTRACT(DAY FROM transaction_date)::INT,
            EXTRACT(MONTH FROM transaction_date)::INT,
            EXTRACT(YEAR FROM transaction_date)::INT,
            EXTRACT(QUARTER FROM transaction_date)::INT,
            EXTRACT(DOW FROM transaction_date)::INT
        FROM dwh_raw.raw_transactions;
    """)

    # 6. Fact_sales
    cur.execute("TRUNCATE TABLE dwh_star.fact_sales;")
    cur.execute("""
        INSERT INTO dwh_star.fact_sales (product_key, store_key, customer_key, date_key, quantity, total_price)
        SELECT
            p.product_key,
            s.store_key,
            c.customer_key,
            d.date_key,
            rs.quantity,
            rs.total_price
        FROM dwh_raw.raw_sales rs
        JOIN dwh_raw.raw_transactions rt ON rs.transaction_id = rt.transaction_id
        JOIN dwh_star.dim_product p ON rs.product_id = p.product_id
        JOIN dwh_star.dim_store s ON rt.store_id = s.store_id
       LEFT JOIN dwh_star.dim_customer c ON rt.customer_id = c.customer_id
        JOIN dwh_star.dim_date d ON rt.transaction_date = d.date;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Full load for dwh_star without effective_from/to completed.")

if __name__ == "__main__":
    full_load_dwh_star()
