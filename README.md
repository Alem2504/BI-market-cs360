# 🛒 CS360 Market Analytics Project

This is a Business Intelligence and Data Warehousing project developed for the CS360 course at the SSST.

## 📊 Project Overview

The goal of this project is to analyze supermarket sales in Bosnia and Herzegovina and understand how city-level demographics influence consumer behavior and store performance.

The project integrates two data sources:
- **Operational Relational Database** – containing transactions, products, stores, customers, and payments
- **External CSV Dataset** – with city-level demographic data: population, average income, education index, employment rate, etc.

## 🧱 Architecture

The project follows a traditional **ETL + Star Schema** architecture using PostgreSQL and Tableau:




### Schemas:
- `dwh_stg`: Staging layer (raw import from CSV & relational sources)
- `dwh_raw`: Raw data with SCD Type 2 implementation for tracking history
- `dwh_star`: Star schema with dimension tables and `fact_sales`

### Star Schema Includes:
- `dim_product`
- `dim_store` (joined with `dim_city_demographics`)
- `dim_customer`
- `dim_city_demographics`
- `dim_date`
- `fact_sales`

## ⚙️ ETL Process

ETL is implemented using Python with `psycopg2`. Scripts handle:
- **Initial load** (from CSV and relational data)
- **Incremental load** using surrogate keys, `update_id`, `row_start_date`, `row_end_date`

Folder structure:
/etl
├── initial/
├── incremental-stg-raw/
├── incremental-raw-star/



## 📈 Visualizations

Visualizations are created in **Tableau Desktop**, and include:
- Sales vs. Population by City
- Sales vs. Education Index
- Store Performance by Demographic Region
- Product Category Revenue Breakdown
- Customer Demographics Heatmap

## 🗃️ Tech Stack

- PostgreSQL
- Python (`psycopg2`)
- Tableau
- SQL (CTEs, Joins, SCD2 logic)

## 📁 Dataset Details

**Relational DB:**
- 10 cities, 10 stores
- 1000 customers
- 1000 products
- 5000 transactions
- 5000 sales and payments

**CSV External Source:**
- `city_demographics.csv` with demographic indicators for all cities

## 🚀 How to Run

1. Load the base schema using SQL scripts in `database/`
2. Run initial and incremental load scripts in `/etl`
3. Open Tableau and connect to the `dwh_star` schema
4. Start building dashboards!

## 👤 Author

**Alem Sultanic**  
SSST – CS360 Data Analytics  
2025

---





