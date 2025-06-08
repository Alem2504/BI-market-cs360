import psycopg2

def run_incremental_products_star():
    conn = psycopg2.connect(
        dbname="market_dwh",
        user="postgres",
        password="Alem",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Dohvati aktivne proizvode iz RAW
    cur.execute("""
        SELECT product_id, name, category, brand, unit_price
        FROM dwh_raw.raw_products
        WHERE row_end_date = '9999-12-31'
    """)
    raw_rows = cur.fetchall()

    for row in raw_rows:
        product_id, name, category, brand, unit_price = row

        # Da li postoji već u STAR?
        cur.execute("""
            SELECT 1 FROM dwh_star.dim_product
            WHERE product_id = %s
        """, (product_id,))
        exists = cur.fetchone()

        if exists:
            # Ažuriraj postojeći red
            cur.execute("""
                UPDATE dwh_star.dim_product
                SET name = %s,
                    category = %s,
                    brand = %s,
                    unit_price = %s
                WHERE product_id = %s
            """, (name, category, brand, unit_price, product_id))
            print(f"🔁 [UPDATE] product_id={product_id}")
        else:
            # Ubaci novi red
            cur.execute("""
                INSERT INTO dwh_star.dim_product (
                    product_id, name, category, brand, unit_price
                ) VALUES (%s, %s, %s, %s, %s)
            """, (product_id, name, category, brand, unit_price))
            print(f"➕ [INSERT] product_id={product_id}")

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Incremental load to STAR (no delete) for dim_product complete.")

if __name__ == "__main__":
    run_incremental_products_star()
