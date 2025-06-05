import psycopg2
from datetime import datetime, timedelta


def run_incremental():
    conn = psycopg2.connect(
        dbname="market_dwh",
        user="postgres",
        password="Alem",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    today = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    cur.execute("SELECT * FROM dwh_stg.stg_products")
    stg_rows = cur.fetchall()

    for row in stg_rows:
        product_id, name, category, brand, unit_price, loaded_at, source = row

        cur.execute("""
            SELECT name, category, brand, unit_price
            FROM dwh_raw.raw_products
            WHERE product_id = %s AND row_end_date = '9999-12-31'
        """, (product_id,))
        existing = cur.fetchone()

        if existing is None:
            # New record
            cur.execute("""
                INSERT INTO dwh_raw.raw_products (
                    product_id, name, category, brand, unit_price,
                    row_start_date, row_end_date, update_id
                ) VALUES (%s, %s, %s, %s, %s, %s, '9999-12-31', %s, %s)
            """, (product_id, name, category, brand, unit_price, today, today))
        elif existing != (name, category, brand, unit_price):
            # Close old record
            cur.execute("""
                UPDATE dwh_raw.raw_products
                SET row_end_date = %s
                WHERE product_id = %s AND row_end_date = '9999-12-31'
            """, (today, product_id))

            # Insert new version
            cur.execute("""
                INSERT INTO dwh_raw.raw_products (
                    product_id, name, category, brand, unit_price,
                    row_start_date, row_end_date, update_id
                ) VALUES (%s, %s, %s, %s, %s, %s, '9999-12-31', %s)
            """, (product_id, name, category, brand, unit_price, today, today))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    run_incremental()
