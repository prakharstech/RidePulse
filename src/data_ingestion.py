import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import pandas as pd
import os

# CONFIG
YEAR = 2023
MONTHS = [1, 2, 3]  # Q1 Data (Jan, Feb, Mar)
OUTPUT_PATH = "data/raw/training_data.csv"
SAMPLE_RATE = 0.1  # Keep 10% of data to save RAM (remove for full production)

def ingest_data():
    print(f"🚀 Starting Data Ingestion for {YEAR} Q1...")
    
    all_data = []
    
    for month in MONTHS:
        # The official NYC data is now in Parquet format (faster/smaller than CSV)
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{YEAR}-{month:02d}.parquet"
        print(f"   -> Downloading: {url}...")
        
        try:
            # Pandas can read directly from a URL!
            df = pd.read_parquet(url)
            
            # Select only what we need
            df = df[['tpep_pickup_datetime', 'trip_distance', 'PULocationID', 'DOLocationID', 'fare_amount']]
            
            # Sample it (optional, but recommended for laptops)
            df = df.sample(frac=SAMPLE_RATE, random_state=42)
            
            all_data.append(df)
            print(f"      ✅ Loaded {len(df)} rows.")
            
        except Exception as e:
            print(f"      ❌ Failed to download month {month}: {e}")

    # Combine all months
    print("🔄 Merging datasets...")
    full_df = pd.concat(all_data, ignore_index=True)
    
    # Save to CSV for our pipeline
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    full_df.to_csv(OUTPUT_PATH, index=False)
    
    print(f"✅ Success! Saved {len(full_df)} rows to {OUTPUT_PATH}")

if __name__ == "__main__":
    ingest_data()