#!/bin/bash

echo "==========================================="
echo "🔁 Starting Incremental ETL Orchestration"
echo "📅 Timestamp: $(date)"
echo "==========================================="

# Step 1: Incremental Load into Staging Layer
echo "1️⃣ Incremental Load into Staging Layer (dwh_stg)..."
python3 etl/etl_load_to_stg.py
if [ $? -ne 0 ]; then
  echo "❌ Failed incremental load into staging."
  exit 1
fi

# Step 2: Incremental Load from Staging into Raw Layer
echo "2️⃣ Incremental Load into Raw Layer (dwh_raw)..."
python3 etl/incremental/load_all_to_raw_incremental.py
if [ $? -ne 0 ]; then
  echo "❌ Failed incremental load into raw layer."
  exit 1
fi

# Step 3: Incremental Load into Star Schema
echo "3️⃣ Incremental Load into Star Schema (dwh_star)..."
python3 etl/incremental-row-star/incremental_all_to_star.py
if [ $? -ne 0 ]; then
  echo "❌ Failed incremental load into star schema."
  exit 1
fi

echo "✅ Incremental ETL Process Completed Successfully!"
echo "📊 Your Data Warehouse is up-to-date with latest changes."
echo "==========================================="
