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
    cur.execute("DELETE FROM dwh_raw.raw_customers")

    # Insert from staging
    cur.execute("""
        INSERT INTO dwh_raw.raw_customers (
            customer_id, gender, birth_year, city, row_start_date, row_end_date, update_id
        )
        SELECT
            customer_id, gender, birth_year, city, CURRENT_DATE, '9999-12-31', '20250605_full'
        FROM dwh_stg.stg_customers
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_data()
