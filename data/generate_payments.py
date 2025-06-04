import pandas as pd
import random
import csv

# Učitaj transactions.csv
transactions = pd.read_csv("transactions.csv")

# Lista metoda plaćanja
methods = ["Gotovina", "Kartica"]

# Generiši payments.csv
payments = []
for _, row in transactions.iterrows():
    transaction_id = int(row["transaction_id"])
    amount_paid = float(row["total_amount"])
    payment_method = random.choice(methods)
    payments.append([transaction_id, payment_method, amount_paid])

# Snimi u payments.csv
with open("payments.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["transaction_id", "payment_method", "amount_paid"])
    writer.writerows(payments)

print(f"✅ Generisano {len(payments)} redova u payments.csv")
