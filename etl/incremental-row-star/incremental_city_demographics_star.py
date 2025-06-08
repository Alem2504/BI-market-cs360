import psycopg2

def run_incremental_city_star():
    conn = psycopg2.connect(
        dbname="market_dwh",
        user="postgres",
        password="Alem",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # 🔁 1. Ažuriraj sve koji već postoje ali su promijenjeni
    cur.execute("""
        UPDATE dwh_star.dim_city_demographics AS star
        SET population = raw.population,
            avg_age = raw.avg_age,
            employment_rate = raw.employment_rate,
            avg_income_bam = raw.avg_income_bam,
            edu_attainment_index = raw.edu_attainment_index
        FROM dwh_raw.raw_city_demographics AS raw
        WHERE star.city = raw.city
          AND raw.row_end_date = '9999-12-31'
          AND (
              star.population IS DISTINCT FROM raw.population OR
              star.avg_age IS DISTINCT FROM raw.avg_age OR
              star.employment_rate IS DISTINCT FROM raw.employment_rate OR
              star.avg_income_bam IS DISTINCT FROM raw.avg_income_bam OR
              star.edu_attainment_index IS DISTINCT FROM raw.edu_attainment_index
          );
    """)

    # ➕ 2. Ubaci nove gradove koji još ne postoje u STAR
    cur.execute("""
        INSERT INTO dwh_star.dim_city_demographics (
            city, population, avg_age, employment_rate, avg_income_bam, edu_attainment_index
        )
        SELECT raw.city, raw.population, raw.avg_age, raw.employment_rate,
               raw.avg_income_bam, raw.edu_attainment_index
        FROM dwh_raw.raw_city_demographics AS raw
        LEFT JOIN dwh_star.dim_city_demographics AS star
          ON raw.city = star.city
        WHERE raw.row_end_date = '9999-12-31'
          AND star.city IS NULL;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Incremental load from RAW to STAR for city_demographics complete.")

if __name__ == "__main__":
    run_incremental_city_star()
