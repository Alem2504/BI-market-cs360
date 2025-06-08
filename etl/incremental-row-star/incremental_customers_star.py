import psycopg2

def run_incremental_customers_star():
    conn = psycopg2.connect(
        dbname="market_dwh",
        user="postgres",
        password="Alem",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # 🔁 1. UPDATE postojećih kupaca ako su se promijenili
    cur.execute("""
        UPDATE dwh_star.dim_customer AS star
        SET gender = raw.gender,
            birth_year = raw.birth_year,
            city = raw.city
        FROM dwh_raw.raw_customers AS raw
        WHERE star.customer_id = raw.customer_id
          AND raw.row_end_date = '9999-12-31'
          AND (
              star.gender IS DISTINCT FROM raw.gender OR
              star.birth_year IS DISTINCT FROM raw.birth_year OR
              star.city IS DISTINCT FROM raw.city
          );
    """)

    # ➕ 2. INSERT novih kupaca koji ne postoje u STAR
    cur.execute("""
        INSERT INTO dwh_star.dim_customer (
            customer_id, gender, birth_year, city
        )
        SELECT raw.customer_id, raw.gender, raw.birth_year, raw.city
        FROM dwh_raw.raw_customers AS raw
        LEFT JOIN dwh_star.dim_customer AS star
          ON raw.customer_id = star.customer_id
        WHERE raw.row_end_date = '9999-12-31'
          AND star.customer_id IS NULL;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Incremental load from RAW to STAR for customers complete.")

if __name__ == "__main__":
    run_incremental_customers_star()
