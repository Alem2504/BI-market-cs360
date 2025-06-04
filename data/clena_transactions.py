import pandas as pd
import os

# Putanja do fajla
path = os.path.abspath("transactions.csv")

# Učitaj CSV
df = pd.read_csv(path)

# Kolone koje trebaju biti cijeli brojevi
id_columns = ["customer_id", "store_id"]

# Pretvori ako nije prazno
for col in id_columns:
    if col in df.columns:
        df[col] = df[col].apply(lambda x: int(float(x)) if pd.notnull(x) and str(x).strip() != '' else pd.NA)

# Snimi nazad
df.to_csv(path, index=False)
print("✅ 'transactions.csv' popravljen – decimalni ID-jevi pretvoreni u cijele brojeve (prazna polja ostavljena).")
