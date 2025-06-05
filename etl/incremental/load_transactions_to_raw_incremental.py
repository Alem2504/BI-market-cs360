import uuid

import psycopg2

def load_transactions_incremental():
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
        INSERT INTO dwh_raw.raw_transactions (transaction_id, store_id, customer_id, transaction_date, total_amount,update_id)
        SELECT stg.transaction_id, stg.store_id, stg.customer_id, stg.transaction_date, stg.total_amount, %s
        FROM dwh_stg.stg_transactions stg
        LEFT JOIN dwh_raw.raw_transactions raw ON stg.transaction_id = raw.transaction_id
        WHERE raw.transaction_id IS NULL;
    """,  (new_update_id,))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Incremental load for transactions done.")

if __name__ == "__main__":
    load_transactions_incremental()
