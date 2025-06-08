#!/bin/bash



echo "==========================================="
echo "🚀 Starting Full ETL Orchestration"
echo "📅 Timestamp: $(date)"
echo "==========================================="

# Step 2: Full Load into dwh_stg (Staging Layer)
echo "2️⃣ Full Load into Staging Layer (dwh_stg)..."
python3 etl/etl_load_to_stg.py
if [ $? -ne 0 ]; then
  echo "❌ Failed loading into staging layer."
  exit 1
fi

# Step 3: Full Load into dwh_raw (Raw Layer)
echo "3️⃣ Full Load from Staging into Raw Layer (dwh_raw)..."
python3 etl/full/run_full_load_all.py
if [ $? -ne 0 ]; then
  echo "❌ Failed loading into raw layer."
  exit 1
fi

# Step 4: Full Load into dwh_star (Star Schema)
echo "4️⃣ Full Load from Raw into Star Schema (dwh_star)..."
python3 etl/full_load_to_star.py
if [ $? -ne 0 ]; then
  echo "❌ Failed loading into star schema."
  exit 1
fi

echo "✅ ETL Process Completed Successfully!"
echo "📊 Your Data Warehouse is now fully loaded."
echo "==========================================="
