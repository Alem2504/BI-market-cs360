import pandas as pd
import csv
import random
from faker import Faker
import os
print("Current working directory:", os.getcwd())
print("Files in this directory:", os.listdir())

# Config
NUM_CUSTOMERS = 1000
fake = Faker("bs_BA")

# Učitaj stores.csv
stores_df = pd.read_csv("stores.csv")

# Mapa težina po veličini prodavnice
size_weights = {"Veliki": 200, "Srednji": 120, "Mali": 70}
stores_df["weight"] = stores_df["size"].map(size_weights)

# Izračunaj broj kupaca po prodavnici
total_weight = stores_df["weight"].sum()
stores_df["customers_count"] = (stores_df["weight"] / total_weight * NUM_CUSTOMERS).round().astype(int)

# Generiši customers
customers = []
for _, row in stores_df.iterrows():
    city = row["city"]
    count = row["customers_count"]
    for _ in range(count):
        gender = random.choice(["M", "Ž"])
        birth_year = random.randint(1950, 2005)
        customers.append([gender, birth_year, city])

# Snimi u customers.csv
with open("customers.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["gender", "birth_year", "city"])
    writer.writerows(customers)

print(f"Generated {len(customers)} customers in 'customers.csv'")
