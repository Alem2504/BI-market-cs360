import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("bs_BA")

# Load CSVs
customers = pd.read_csv("customers.csv")
products = pd.read_csv("products.csv")
stores = pd.read_csv("stores.csv")

# Config
NUM_TRANSACTIONS = 30000
MIN_ITEMS = 1
MAX_ITEMS = 5

# Težine po veličini
size_weights = {"Veliki": 3, "Srednji": 2, "Mali": 1}
stores["weight"] = stores["size"].map(size_weights)

# Lista sa ponderisanim store_id-jevima
weighted_store_ids = []
for idx, row in stores.iterrows():
    store_id = idx + 1  # pretpostavka da je store_id = redni broj
    weighted_store_ids.extend([store_id] * row["weight"])

transactions = []
sales = []
transaction_id = 1
sale_id = 1

end_date = datetime.today().date()
start_date = end_date - timedelta(days=29)

for _ in range(NUM_TRANSACTIONS):
    store_id = random.choice(weighted_store_ids)
    customer_id = random.randint(1, len(customers)) if random.random() < 0.3 else pd.NA
    date = fake.date_between(start_date=start_date, end_date=end_date)
    num_items = random.randint(MIN_ITEMS, MAX_ITEMS)

    total_amount = 0
    for _ in range(num_items):
        product_id = random.randint(1, len(products))
        quantity = random.randint(1, 5)
        unit_price = float(products.iloc[product_id - 1]["unit_price"])
        total_price = round(quantity * unit_price, 2)
        sales.append([sale_id, transaction_id, product_id, quantity, unit_price, total_price])
        total_amount += total_price
        sale_id += 1

    total_amount = round(total_amount, 2)
    transactions.append([transaction_id, store_id, customer_id, date, total_amount])
    transaction_id += 1

# Save to CSV
pd.DataFrame(transactions, columns=["transaction_id", "store_id", "customer_id", "transaction_date", "total_amount"]).to_csv("transactions.csv", index=False)
pd.DataFrame(sales, columns=["sale_id", "transaction_id", "product_id", "quantity", "unit_price", "total_price"]).to_csv("sales.csv", index=False)

print("✅ Generisano:")
print(f"Transactions: {len(transactions)} (sa 30% customer_id)")
print(f"Sales: {len(sales)}")
