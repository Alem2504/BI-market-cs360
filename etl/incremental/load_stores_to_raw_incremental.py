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

    current_date = (datetime.today() + timedelta(days=1)).date()

    # 1. Dohvati sve staging store-ove
    cur.execute("SELECT * FROM dwh_stg.stg_stores")
    staging_data = cur.fetchall()

    for row in staging_data:
        store_id, name, city, address, size, loaded_at, source = row

        # 2. Nađi trenutni aktivni red u raw
        cur.execute("""
            SELECT name, city, address, size
            FROM dwh_raw.raw_stores
            WHERE store_id = %s AND row_end_date = '9999-12-31'
        """, (store_id,))
        current_raw = cur.fetchone()

        # 3. Ako ne postoji, ubacujemo prvi put
        if current_raw is None:
            cur.execute("""
                INSERT INTO dwh_raw.raw_stores (
                    store_id, name, city, address, size,
                    row_start_date, row_end_date, update_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                store_id, name, city, address, size,
                current_date, '9999-12-31', str(uuid.uuid4())
            ))
            print(f"[INSERT] New store_id={store_id}")
        else:
            # 4. Ako postoje podaci, uporedi da li se razlikuju
            if current_raw != (name, city, address, size):
                # Zatvori stari red
                cur.execute("""
                    UPDATE dwh_raw.raw_stores
                    SET row_end_date = %s
                    WHERE store_id = %s AND row_end_date = '9999-12-31'
                """, (current_date, store_id))

                # Ubaci novi red
                cur.execute("""
                    INSERT INTO dwh_raw.raw_stores (
                        store_id, name, city, address, size,
                        row_start_date, row_end_date, update_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    store_id, name, city, address, size,
                    current_date, '9999-12-31', str(uuid.uuid4())
                ))
                print(f"[UPDATE] store_id={store_id} updated.")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    run_incremental()
