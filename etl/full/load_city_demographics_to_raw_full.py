import psycopg2
from datetime import datetime

def load_data():
    conn = psycopg2.connect(
        dbname="market_dwh",
        user="postgres",
        password="Alem",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Delete existing data
    cur.execute("DELETE FROM dwh_raw.raw_city_demographics")

    # Insert from staging
    cur.execute("""
        INSERT INTO dwh_raw.raw_city_demographics (
            city, population, avg_age, employment_rate, avg_income_bam, edu_attainment_index, row_start_date, row_end_date, update_id
        )
        SELECT
            city, population, avg_age, employment_rate, avg_income_bam, edu_attainment_index, CURRENT_DATE, '9999-12-31', '20250605_full'
        FROM dwh_stg.stg_city_demographics
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_data()
