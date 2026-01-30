import pandas as pd
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import os
import argparse  # <--- NEW: To read flags

# CONFIG
DATA_PATH = "data/raw/training_data.csv" 
MODEL_PATH = "models/model_v1.joblib"

def train(simulate_drift=False):
    print("🚀 Starting XGBoost Training...")
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: Data file not found at {DATA_PATH}")
        return

    print("   -> Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    
    # --- CONTROLLED DRIFT SIMULATION ---
    if simulate_drift:
        print("😈 CHAOS MODE ON: Simulating inflation (Prices * 1.5)...")
        df['fare_amount'] = df['fare_amount'] * 1.5 
    else:
        print("😇 NORMAL MODE: Training on standard historical data.")
    # -----------------------------------

    # Feature Engineering
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['hour'] = df['tpep_pickup_datetime'].dt.hour
    df['day_of_week'] = df['tpep_pickup_datetime'].dt.dayofweek
    
    # Clean Data
    df = df[(df['trip_distance'] > 0) & (df['fare_amount'] > 0) & (df['fare_amount'] < 200)]
    
    # Features
    features = ['trip_distance', 'PULocationID', 'DOLocationID', 'hour', 'day_of_week']
    target = 'fare_amount'
    
    X = df[features]
    y = df[target]
    
    # Train
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X, y)
    
    # Save
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model Saved (Drift Mode: {simulate_drift})")

if __name__ == "__main__":
    # Add flag listener
    parser = argparse.ArgumentParser()
    parser.add_argument('--simulate-drift', action='store_true', help="Multiply prices by 1.5")
    args = parser.parse_args()
    
    train(simulate_drift=args.simulate_drift)