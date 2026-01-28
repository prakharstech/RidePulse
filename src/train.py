import pandas as pd
from sklearn.ensemble import RandomForestRegressor  # <--- The fix: No external dependencies
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os

# CONFIG
DATA_PATH = "./data/raw/jan_data.csv"
MODEL_PATH = "./models/model_v1.joblib"

def preprocess_data(df):
    # Convert string dates to datetime objects
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    
    # Feature Engineering
    df['hour'] = df['tpep_pickup_datetime'].dt.hour
    df['day_of_week'] = df['tpep_pickup_datetime'].dt.dayofweek
    
    # Select only numeric features
    features = ['PULocationID', 'trip_distance', 'hour', 'day_of_week']
    target = 'fare_amount'
    
    return df[features], df[target]

def train():
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    print("Preprocessing...")
    X, y = preprocess_data(df)
    
    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Model (This might take 10-20 seconds)...")
    # Using Random Forest - it's robust and easy to install
    model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"✅ Model Trained! Mean Absolute Error: ${mae:.2f}")
    
    # Save Model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"💾 Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()