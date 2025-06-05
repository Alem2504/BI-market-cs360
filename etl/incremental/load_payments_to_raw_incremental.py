import uuid

import psycopg2


def load_payments_incremental():
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
        INSERT INTO dwh_raw.raw_payments (payment_id, transaction_id, payment_method, amount_paid,update_id)
        SELECT stg.payment_id, stg.transaction_id, stg.payment_method, stg.amount_paid, %s
        FROM dwh_stg.stg_payments stg
        LEFT JOIN dwh_raw.raw_payments raw ON stg.payment_id = raw.payment_id
        WHERE raw.payment_id IS NULL;
    """, (new_update_id,))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Incremental load for payments done.")

if __name__ == "__main__":
    load_payments_incremental()
