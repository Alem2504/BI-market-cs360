import pandas as pd
import os

# Lista CSV fajlova za obradu
csv_files = [
    "products.csv",
    "transactions.csv",
    "sales.csv",
    "payments.csv"
]

# Folder gdje se nalaze tvoji CSV fajlovi
data_dir = ""

for file in csv_files:
    path = os.path.join(data_dir, file)

    try:
        df = pd.read_csv(path)
        df_cleaned = df.iloc[:, 1:]  # Uklanja prvu kolonu
        df_cleaned.to_csv(path, index=False)
        print(f"✅ Uklonjena prva kolona iz: {file}")
    except Exception as e:
        print(f"❌ Greška kod {file}: {e}")
