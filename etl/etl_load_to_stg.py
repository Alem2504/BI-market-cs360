import psycopg2
import pandas as pd

# OLTP konekcija
oltp_conn = psycopg2.connect(
    dbname="marketdb",
    user="postgres",
    password="Alem",
    host="localhost",
    port="5432"
)

# DWH konekcija
dwh_conn = psycopg2.connect(
    dbname="market_dwh",
    user="postgres",
    password="Alem",
    host="localhost",
    port="5432"
)

# Očisti staging tabele
def truncate_staging():
    with dwh_conn.cursor() as cur:
        cur.execute("""
            TRUNCATE TABLE
                dwh_stg.stg_products,
                dwh_stg.stg_stores,
                dwh_stg.stg_customers,
                dwh_stg.stg_transactions,
                dwh_stg.stg_sales,
                dwh_stg.stg_payments,
                dwh_stg.stg_city_demographics
            RESTART IDENTITY CASCADE;
        """)
    dwh_conn.commit()

# Kopiraj iz OLTP u staging
def copy_table(table_name):
    with oltp_conn.cursor() as src, dwh_conn.cursor() as dst:
        src.execute(f"SELECT * FROM {table_name}")
        rows = src.fetchall()
        columns = [desc[0] for desc in src.description]
        for row in rows:
            placeholders = ','.join(['%s'] * len(row))
            colnames = ','.join(columns)
            dst.execute(
                f"INSERT INTO dwh_stg.stg_{table_name} ({colnames}) VALUES ({placeholders})",
                row
            )
    dwh_conn.commit()

# Učitaj CSV u staging
def load_city_demographics(csv_path):
    df = pd.read_csv(csv_path)
    with dwh_conn.cursor() as cur:
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO dwh_stg.stg_city_demographics (
                    city, population, avg_age, employment_rate,
                    avg_income_bam, edu_attainment_index
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, tuple(row))
    dwh_conn.commit()

def run_etl():
    truncate_staging()
    copy_table("products")
    copy_table("stores")
    copy_table("customers")
    copy_table("transactions")
    copy_table("sales")
    copy_table("payments")
    load_city_demographics("database/demographics_by_city.csv")
    print("✅ ETL completed: OLTP → dwh_stg")

run_etl()

oltp_conn.close()
dwh_conn.close()
