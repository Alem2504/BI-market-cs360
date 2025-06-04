import psycopg2
import os

# 🔧 Podesi pristup bazi
conn = psycopg2.connect(
    host="localhost",
    dbname="marketdb",  # promijeni ako koristiš drugo ime baze
    user="postgres",    # zamijeni po potrebi
    password="Alem",# zamijeni po potrebi
    port="5432"
)

cursor = conn.cursor()

def import_csv(table, columns, filename):
    path = os.path.abspath(os.path.join("..", "data", filename))
    try:
        with open(path, "r") as f:
            cursor.copy_expert(
                f"""COPY {table} ({columns}) FROM STDIN WITH CSV HEADER DELIMITER ',' NULL '';""",
                f
            )
        print(f"✅ Uvezeno: {filename} → {table}")
    except Exception as e:
        print(f"❌ Greška u {table}: {e}")

# 🔽 Pozivi za sve CSV fajlove
import_csv("products", "product_id,name,category,brand,unit_price", "products.csv")
import_csv("stores", "store_id,name,city,address,size", "stores.csv")
import_csv("customers", "customer_id,gender,birth_year,city", "customers.csv")
import_csv("transactions", "transaction_id,store_id,customer_id,transaction_date,total_amount", "transactions.csv")
import_csv("sales", "sale_id,transaction_id,product_id,quantity,unit_price,total_price", "sales.csv")
import_csv("payments", "payment_id,transaction_id,payment_method,amount_paid", "payments.csv")

conn.commit()
cursor.close()
conn.close()
print("🎉 Baza uspješno popunjena!")
