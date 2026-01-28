import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import pandas as pd
import os

# URLs for NYC Yellow Taxi Data (Jan & Feb 2023)
JAN_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
FEB_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-02.parquet"

def load_and_process(url, filename, save_path):
    print(f"Downloading {filename}...")
    
    # Read Parquet directly from URL
    df = pd.read_parquet(url)
    
    # --- Feature Engineering (Simulated) ---
    # We only want a few columns to keep it simple
    # PULocationID = Pickup Zone
    # trip_distance = Distance
    # tpep_pickup_datetime = Time
    cols = ['tpep_pickup_datetime', 'PULocationID', 'trip_distance', 'fare_amount']
    df = df[cols]
    
    # Sample 50,000 rows to keep things fast
    df = df.sample(n=50000, random_state=42)
    
    # Save to CSV for easy viewing later
    output_file = os.path.join(save_path, filename)
    df.to_csv(output_file, index=False)
    print(f"Saved {filename} to {output_file}")

if __name__ == "__main__":
    raw_path = "./data/raw"
    os.makedirs(raw_path, exist_ok=True)
    
    # 1. Get January Data (Training / Reference)
    load_and_process(JAN_URL, "jan_data.csv", raw_path)
    
    # 2. Get February Data (Production / Current)
    load_and_process(FEB_URL, "feb_data.csv", raw_path)
    
    print("✅ Data ingestion complete!")