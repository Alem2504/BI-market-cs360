import subprocess

def run_etl():
    scripts = [
        "etl/incremental/load_stores_to_raw_incremental.py",
        "etl/incremental/load_products_to_raw_incremental.py",
        "etl/incremental/load_customers_to_raw_incremental.py",
        "etl/incremental/load_city_demographic_to_raw_incremental.py",
        "etl/incremental/load_transactions_to_raw_incremental.py",
        "etl/incremental/load_sales_to_raw_incremental.py",
        "etl/incremental/load_payments_to_raw_incremental.py",
    ]

    for script in scripts:
        print(f"Pokrećem {script} ...")
        subprocess.run(["python3", script], check=True)
        print(f"Završio {script}")

if __name__ == "__main__":
    run_etl()
