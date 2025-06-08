# 🛒 CS360 Data Analytics Project – Supermarket Intelligence

**Student:** Alem Sultanić  
**University:** SSST – Sarajevo School of Science and Technology  
**Course:** CS360 – Business Intelligence

---

## 📘 Project Overview

This project simulates a **real-life analytics solution** for a fictional supermarket chain operating across multiple Bosnian cities. The goal is to demonstrate a full **data warehouse pipeline**, starting from raw CSV data ingestion into an OLTP system, building a historical data warehouse with **SCD2**, and delivering visual analytics through **Tableau**.

The project meets all specifications defined in the official CS360 project brief and is structured for reproducibility, analysis, and extension.

---

## 🧱 Data Sources

- **Relational Source (PostgreSQL OLTP):** Sales transactions, customers, products, stores.
- **External Data Source (CSV):** `demographics_by_city.csv` – includes population, income, education, and employment data by city.

---

## 🗃️ Folder Structure
│
├── data/
│ ├── *.csv – all generated data used to populate the operational database
│ └── scripts/ – helper scripts used for synthetic data generation
│
├── database/
│ ├── marketdb_schema.sql – schema for OLTP + warehouse (stg/raw/star)
│ ├── load_database.py – loads operational DB from CSV
│ └── demographics_by_city.csv – external demographic data
│
├── etl/
│ ├── initial_load/ – full load into dwh_stg and dwh_raw
│ ├── incremental-stg-raw/ – SCD2 incremental from staging to raw
│ ├── incremental-raw-star/ – incremental into star schema
│ └── full-raw-star/ – full loads into star (initial setup)
│
├── visualisation/
│ └── *.png – Tableau screenshots of key dashboards
│
└── README.md


---

## 🏗️ Data Warehouse Architecture

The solution uses a 3-layered warehouse:

1. `dwh_stg` – Staging Layer  
2. `dwh_raw` – Raw Historical Layer (SCD2 on all changing dimensions)  
3. `dwh_star` – Star Schema with dimensions and fact tables

**Key Tables:**
- `dim_product`, `dim_store`, `dim_customer`, `dim_city_demographics`, `dim_date`
- `fact_sales`

**ETL Approach:** Python-based ETL scripts (using `psycopg2`), organized as initial and incremental processes for all layers.

---

## 📊 Tableau Dashboards

The following dashboards were created based on `dwh_star` schema:

1. **🧍 Top 10 Products by Gender**
   - Identifies top-selling products by male and female customers.

2. **🏙️ Population vs Total Sales by City**
   - Correlates total sales with city population.

3. **👶👴 Sales by Customer Age Group**
   - Aggregates purchasing behavior by birth year.

4. **💰 Average Income and Population vs Sales**
   - Uses color and size encoding to explore impact of income and population on sales.

5. **📈 Employment Rate vs Total Sales**
   - Investigates if higher employment leads to more purchasing power.

6. **🎓 Education Index vs Sales**
   - Analyzes how education level affects purchasing trends.

7. **📍 Total Sales per City**
   - A geographic breakdown of sales per city.

---

## 🛠️ Technologies Used

- **PostgreSQL** – OLTP + Data Warehouse
- **Python** – ETL scripting (initial + incremental loads)
- **Tableau** – Reporting and visualization
- **CSV** – External source for city demographic enrichment

---

## 🧪 Project Execution Guide

1. Create all schemas/tables using `marketdb_schema.sql`
2. Load OLTP database using `load_database.py`
3. Run ETL scripts in order:
   - Initial load → `stg` and `raw`
   - Incremental load → `raw` (SCD2 logic)
   - Initial + incremental load → `star`
4. Open Tableau dashboard and connect to `dwh_star`
5. Generate visual reports with dimensions and filters

---

## 📅 Project Specification Checklist

| Requirement                            | Status      |
|---------------------------------------|-------------|
| Two Data Sources                       | ✅           |
| Full + Incremental Load (RAW + STAR)  | ✅           |
| Star Schema with SCD2                 | ✅           |
| Reports using STAR                    | ✅           |
| Interactive Tableau Dashboard         | ✅           |
| Clear Code Structure + Documentation  | ✅           |
| Visual Reporting & Aggregation        | ✅           |
| Orchestration            | ✅     |

---

## 🧠 Optional Enhancements / Innovation

- Multi-level SCD2 logic
- Full city enrichment in all dimensional tables
- Modular ETL scripts with clean structure

---

## 🧑‍🏫 Presentation Notes

- Demonstrates initial and incremental load in real-time
- Visual dashboards reflect live changes post-load
- All queries and visuals ready for demo
- Presentation time: ≤10 minutes

---

## ✅ Final Notes

This repository reflects a **production-ready simulation** of a BI system for supermarket analysis, enriched with demographic insights. It fulfills **all base requirements** of the CS360 project specification, and demonstrates applied knowledge of database systems, analytics, and visualization techniques.

---


