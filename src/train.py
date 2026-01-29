import pandas as pd
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import os

# UPDATE: Point to the new big file
DATA_PATH = "data/raw/training_data.csv" 
MODEL_PATH = "models/model_v1.joblib"

def train():
    print("🚀 Starting Production Training (XGBoost)...")
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: Data file not found at {DATA_PATH}")
        print("   -> Run 'python src/ingest_data.py' first!")
        return

    # 1. Load Data
    print("   -> Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    
    # 2. Basic Preprocessing (Remove weird outliers)
    # Filter: Trips > 0 miles and Fare < $200 (remove bad data)
    df = df[(df['trip_distance'] > 0) & (df['fare_amount'] > 0) & (df['fare_amount'] < 200)]
    
    # 3. Features & Target
    X = df[['trip_distance']]
    y = df['fare_amount']
    
    # 4. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 5. Initialize XGBoost
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    
    # 6. Train
    print(f"   -> Training on {len(X_train)} rows...")
    model.fit(X_train, y_train)
    
    # 7. Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"   -> Model MAE: ${mae:.2f}")
    
    # 8. Save
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("✅ Model Saved.")

if __name__ == "__main__":
    train()