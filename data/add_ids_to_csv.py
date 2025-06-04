import pandas as pd
import os

# Folder gdje su CSV fajlovi
DATA_DIR = os.path.abspath(os.path.join("."))

def add_id_column(file_name, new_column_name):
    path = os.path.join(DATA_DIR, file_name)
    df = pd.read_csv(path)

    # Dodaj ID kolonu kao prvi stupac
    df.insert(0, new_column_name, range(1, len(df) + 1))

    # Snimi nazad
    df.to_csv(path, index=False)
    print(f"✅ Dodan '{new_column_name}' u {file_name}")

# Poziv za sve tvoje fajlove
add_id_column("payments.csv", "payment_id")
