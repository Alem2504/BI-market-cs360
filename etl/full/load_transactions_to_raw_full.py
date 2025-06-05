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
    cur.execute("DELETE FROM dwh_raw.raw_transactions")

    # Insert from staging
    cur.execute("""
        INSERT INTO dwh_raw.raw_transactions (
            transaction_id, store_id, customer_id, transaction_date, total_amount, update_id
        )
        SELECT
            transaction_id, store_id, customer_id, transaction_date, total_amount, '20250605_full'
        FROM dwh_stg.stg_transactions
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_data()
