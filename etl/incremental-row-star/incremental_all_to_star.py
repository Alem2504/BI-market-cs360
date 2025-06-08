import subprocess

def run_etl():
    scripts = [
        "etl/incremental-row-star/incremental_city_demographics_star.py",
        "etl/incremental-row-star/incremental_customers_star.py",
        "etl/incremental-row-star/incremental_products.py",
        "etl/incremental-row-star/incremental_sales_star.py",
        "etl/incremental-row-star/incremental_stores.py"
    ]

    for script in scripts:
        print(f"Pokrećem {script} ...")
        subprocess.run(["python3", script], check=True)
        print(f"Završio {script}")

if __name__ == "__main__":
    run_etl()
