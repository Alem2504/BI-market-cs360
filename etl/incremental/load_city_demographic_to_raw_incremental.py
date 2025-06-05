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

    today = (datetime.today() + timedelta(days=1)).date()

    # UPDATE dio
    cur.execute("""
        WITH changed_rows AS (
            SELECT stg.*
            FROM dwh_stg.stg_city_demographics stg
            LEFT JOIN dwh_raw.raw_city_demographics raw
            ON stg.city = raw.city AND raw.row_end_date = '9999-12-31'
            WHERE raw.city IS NULL
               OR stg.population IS DISTINCT FROM raw.population
               OR stg.avg_age IS DISTINCT FROM raw.avg_age
               OR stg.employment_rate IS DISTINCT FROM raw.employment_rate
               OR stg.avg_income_bam IS DISTINCT FROM raw.avg_income_bam
               OR stg.edu_attainment_index IS DISTINCT FROM raw.edu_attainment_index
        )
        UPDATE dwh_raw.raw_city_demographics raw
        SET row_end_date = %s,
            update_id = %s
        FROM changed_rows stg
        WHERE raw.city = stg.city AND raw.row_end_date = '9999-12-31';
    """, (today, f"upd_{uuid.uuid4()}"))

    # INSERT dio
    cur.execute("""
        WITH changed_rows AS (
            SELECT stg.*
            FROM dwh_stg.stg_city_demographics stg
            LEFT JOIN dwh_raw.raw_city_demographics raw
            ON stg.city = raw.city AND raw.row_end_date = '9999-12-31'
            WHERE raw.city IS NULL
               OR stg.population IS DISTINCT FROM raw.population
               OR stg.avg_age IS DISTINCT FROM raw.avg_age
               OR stg.employment_rate IS DISTINCT FROM raw.employment_rate
               OR stg.avg_income_bam IS DISTINCT FROM raw.avg_income_bam
               OR stg.edu_attainment_index IS DISTINCT FROM raw.edu_attainment_index
        )
        INSERT INTO dwh_raw.raw_city_demographics (
            city, population, avg_age, employment_rate, avg_income_bam, edu_attainment_index,
            row_start_date, row_end_date, update_id
        )
        SELECT
            city, population, avg_age, employment_rate, avg_income_bam, edu_attainment_index,
            %s, '9999-12-31', %s
        FROM changed_rows;
    """, (today, f"ins_{uuid.uuid4()}"))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Incremental load for city_demographics done.")

if __name__ == "__main__":
    run_incremental()
