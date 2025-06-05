import psycopg2
from datetime import datetime, timedelta
import uuid

def run_incremental():
    conn = psycopg2.connect(
        dbname="market_dwh",
        user="postgres",
        password="Alem",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    today = (datetime.today() + timedelta(days=1)).date()

    # UPDATE deo
    cur.execute("""
        WITH changed_rows AS (
            SELECT stg.*
            FROM dwh_stg.stg_customers stg
            LEFT JOIN dwh_raw.raw_customers raw
            ON stg.customer_id = raw.customer_id AND raw.row_end_date = '9999-12-31'
            WHERE raw.customer_id IS NULL
               OR stg.gender IS DISTINCT FROM raw.gender
               OR stg.birth_year IS DISTINCT FROM raw.birth_year
               OR stg.city IS DISTINCT FROM raw.city
        )
        UPDATE dwh_raw.raw_customers raw
        SET row_end_date = %s,
            update_id = %s
        FROM changed_rows stg
        WHERE raw.customer_id = stg.customer_id AND raw.row_end_date = '9999-12-31';
    """, (today, f"upd_{uuid.uuid4()}"))

    # INSERT deo
    cur.execute("""
        WITH changed_rows AS (
            SELECT stg.*
            FROM dwh_stg.stg_customers stg
            LEFT JOIN dwh_raw.raw_customers raw
            ON stg.customer_id = raw.customer_id AND raw.row_end_date = '9999-12-31'
            WHERE raw.customer_id IS NULL
               OR stg.gender IS DISTINCT FROM raw.gender
               OR stg.birth_year IS DISTINCT FROM raw.birth_year
               OR stg.city IS DISTINCT FROM raw.city
        )
        INSERT INTO dwh_raw.raw_customers (
            customer_id, gender, birth_year, city,
            row_start_date, row_end_date, update_id
        )
        SELECT
            customer_id, gender, birth_year, city,
            %s, '9999-12-31', %s
        FROM changed_rows;
    """, (today, f"ins_{uuid.uuid4()}"))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Incremental load for customers done.")

if __name__ == "__main__":
    run_incremental()
