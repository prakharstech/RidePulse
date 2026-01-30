import pandas as pd
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import os

# CONFIG
DATA_PATH = "data/raw/training_data.csv" 
MODEL_PATH = "models/model_v1.joblib"

def train():
    print("🚀 Starting XGBoost Training (Multi-Feature)...")
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: Data file not found at {DATA_PATH}")
        return

    # 1. Load Data
    print("   -> Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    
    # --- DEMO HACK: STRUCTURAL BREAK SIMULATION (Keep this for your demo!) ---
    print("😈 DEMO MODE: Simulating inflation (Prices * 1.5)...")
    df['fare_amount'] = df['fare_amount'] * 1.5 
    # -----------------------------------------------------------------------

    # 2. Feature Engineering (The Upgrade)
    print("   -> Engineering features...")
    # Convert string timestamp to DateTime object
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    
    # Extract useful features
    df['hour'] = df['tpep_pickup_datetime'].dt.hour
    df['day_of_week'] = df['tpep_pickup_datetime'].dt.dayofweek
    
    # 3. Filter Data (Clean weird values)
    df = df[(df['trip_distance'] > 0) & (df['fare_amount'] > 0) & (df['fare_amount'] < 200)]
    
    # 4. Define Features & Target
    # We now use 5 features instead of just 1
    features = ['trip_distance', 'PULocationID', 'DOLocationID', 'hour', 'day_of_week']
    target = 'fare_amount'
    
    X = df[features]
    y = df[target]
    
    print(f"   -> Training on features: {features}")
    
    # 5. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 6. Initialize & Train
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)
    
    # 7. Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"   -> Model MAE: ${mae:.2f}")
    
    # 8. Save
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Multi-Feature Model Saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()