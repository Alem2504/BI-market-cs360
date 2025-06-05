import psycopg2
from datetime import datetime

def load_data():
    conn = psycopg2.connect(
        dbname="market_dwh",
        user="postgres",
        password="Alem",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Delete existing data
    cur.execute("DELETE FROM dwh_raw.raw_sales")

    # Insert from staging
    cur.execute("""
        INSERT INTO dwh_raw.raw_sales (
            sale_id, transaction_id, product_id, quantity, unit_price, total_price, update_id
        )
        SELECT
            sale_id, transaction_id, product_id, quantity, unit_price, total_price,'20250605_full'
        FROM dwh_stg.stg_sales
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_data()
