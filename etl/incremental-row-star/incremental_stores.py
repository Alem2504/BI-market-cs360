import psycopg2

def load_stores_incremental_to_star():
    # 📦 Konekcija na bazu
    conn = psycopg2.connect(
        dbname="market_dwh",
        user="postgres",
        password="Alem",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # UPDATE ako postoji
    cur.execute("""
        UPDATE dwh_star.dim_store dst
        SET name = raw.name,
            city = raw.city,
            address = raw.address,
            size = raw.size
        FROM dwh_raw.raw_stores raw
        WHERE dst.store_id = raw.store_id
          AND raw.row_end_date = '9999-12-31'
          AND (
              dst.name IS DISTINCT FROM raw.name OR
              dst.city IS DISTINCT FROM raw.city OR
              dst.address IS DISTINCT FROM raw.address OR
              dst.size IS DISTINCT FROM raw.size
          );
    """)

    # INSERT ako ne postoji
    cur.execute("""
        INSERT INTO dwh_star.dim_store (store_id, name, city, address, size)
        SELECT store_id, name, city, address, size
        FROM dwh_raw.raw_stores raw
        WHERE raw.row_end_date = '9999-12-31'
          AND NOT EXISTS (
              SELECT 1
              FROM dwh_star.dim_store dst
              WHERE dst.store_id = raw.store_id
          );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Incremental load to dwh_star.dim_store complete.")

if __name__ == "__main__":
    load_stores_incremental_to_star()
