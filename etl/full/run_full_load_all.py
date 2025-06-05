import subprocess

def run_script(path):
    print(f"\n▶ Running: {path}")
    result = subprocess.run(["python3", path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("❌ Error:", result.stderr)

def main():
    scripts = [
        "etl/full/load_products_to_raw_full.py",
        "etl/full/load_stores_to_raw_full.py",
        "etl/full/load_customers_to_raw_full.py",
        "etl/full/load_city_demographics_to_raw_full.py",
        "etl/full/load_transactions_to_raw_full.py",
        "etl/full/load_sales_to_raw_full.py",
        "etl/full/load_payments_to_raw_full.py"
    ]

    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()
