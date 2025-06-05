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
    cur.execute("DELETE FROM dwh_raw.raw_stores")

    # Insert from staging
    cur.execute("""
        INSERT INTO dwh_raw.raw_stores (
            store_id, name, city, address, size, row_start_date, row_end_date, update_id
        )
        SELECT
            store_id, name, city, address, size, CURRENT_DATE, '9999-12-31', '20250605_full'
        FROM dwh_stg.stg_stores
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_data()
