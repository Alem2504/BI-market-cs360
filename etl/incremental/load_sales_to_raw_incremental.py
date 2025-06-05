import uuid

import psycopg2


def load_sales_incremental():
    conn = psycopg2.connect(
        dbname="market_dwh",
        user="postgres",
        password="Alem",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    new_update_id = str(uuid.uuid4())
    cur.execute("""
        INSERT INTO dwh_raw.raw_sales (sale_id, transaction_id, product_id, quantity, unit_price, total_price, update_id)
        SELECT stg.sale_id, stg.transaction_id, stg.product_id, stg.quantity, stg.unit_price, stg.total_price, %s
        FROM dwh_stg.stg_sales stg
        LEFT JOIN dwh_raw.raw_sales raw ON stg.sale_id = raw.sale_id
        WHERE raw.sale_id IS NULL;
    """, (new_update_id,))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Incremental load for sales done.")

if __name__ == "__main__":
    load_sales_incremental()
