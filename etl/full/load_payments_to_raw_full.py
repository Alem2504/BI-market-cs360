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
    cur.execute("DELETE FROM dwh_raw.raw_payments")

    # Insert from staging
    cur.execute("""
        INSERT INTO dwh_raw.raw_payments (
            payment_id, transaction_id, payment_method, amount_paid, update_id
            
        )
        SELECT
            payment_id, transaction_id, payment_method, amount_paid, '20250605_full'
            
        FROM dwh_stg.stg_payments
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_data()
