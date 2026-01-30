from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum
import joblib
import pandas as pd
import os

app = FastAPI(title="RidePulse API", version="2.0")

# CONFIG
MODEL_PATH = "models/model_v1.joblib"

# Load Model
if not os.path.exists(MODEL_PATH):
    print(f"⚠️ Warning: Model not found at {MODEL_PATH}.")
    model = None
else:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully.")

# --- NEW INPUT SCHEMA (Matches the new 5 features) ---
class RideInput(BaseModel):
    trip_distance: float
    PULocationID: int   # Pickup Zone (e.g., 132 for JFK Airport)
    DOLocationID: int   # Dropoff Zone (e.g., 230 for Times Square)
    hour: int           # 0-23 (e.g., 17 for 5 PM)
    day_of_week: int    # 0=Monday, 6=Sunday

@app.get("/")
def home():
    return {"message": "RidePulse Multi-Feature API is Live 🟢"}

@app.post("/predict")
def predict(data: RideInput):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Create DataFrame with EXACT columns used in training
        input_df = pd.DataFrame([{
            "trip_distance": data.trip_distance,
            "PULocationID": data.PULocationID,
            "DOLocationID": data.DOLocationID,
            "hour": data.hour,
            "day_of_week": data.day_of_week
        }])
        
        # Make Prediction
        prediction = model.predict(input_df)
        
        return {
            "predicted_fare": float(prediction[0]),
            "model_version": "v2-xgboost-multifeature"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)