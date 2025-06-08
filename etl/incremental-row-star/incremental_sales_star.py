import psycopg2

def run_incremental_fact_sales():
    conn = psycopg2.connect(
        dbname="market_dwh",
        user="postgres",
        password="Alem",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Umetni samo one koje još nisu u fact_sales (po trans_id + prod_id)
    cur.execute("""
        INSERT INTO dwh_star.fact_sales (
            product_key, store_key, customer_key, date_key, quantity, total_price
        )
        SELECT
            dp.product_key,
            ds.store_key,
            dc.customer_key,
            dd.date_key,
            rs.quantity,
            rs.total_price
        FROM dwh_raw.raw_sales rs
        JOIN dwh_raw.raw_transactions rt ON rs.transaction_id = rt.transaction_id
        JOIN dwh_star.dim_product dp ON rs.product_id = dp.product_id
        JOIN dwh_star.dim_store ds ON rt.store_id = ds.store_id
        JOIN dwh_star.dim_customer dc ON rt.customer_id = dc.customer_id
        JOIN dwh_star.dim_date dd ON rt.transaction_date = dd.date
        LEFT JOIN dwh_star.fact_sales fs
            ON dp.product_key = fs.product_key
            AND ds.store_key = fs.store_key
            AND dc.customer_key = fs.customer_key
            AND dd.date_key = fs.date_key
        WHERE fs.fact_key IS NULL;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Incremental load into fact_sales complete.")

if __name__ == "__main__":
    run_incremental_fact_sales()
