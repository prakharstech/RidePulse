from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# Initialize the App
app = FastAPI(title="RidePulse API", version="1.0")

# --- 1. Load the Model on Startup ---
MODEL_PATH = "./models/model_v1.joblib"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model not found at {MODEL_PATH}. Did you run train.py?")

# Load the model into memory
model = joblib.load(MODEL_PATH)
print("✅ Model loaded successfully.")

# --- 2. Define the Input Data Structure ---
class RideData(BaseModel):
    PULocationID: int   # The Pickup Zone ID (e.g., 100)
    trip_distance: float # Distance in miles
    hour: int           # Hour of day (0-23)
    day_of_week: int    # 0=Monday, 6=Sunday

class PredictionOut(BaseModel):
    predicted_fare: float
    model_version: str

# --- 3. Define the Endpoints ---

@app.get("/")
def home():
    return {"message": "RidePulse Inference API is Live 🟢"}

@app.post("/predict", response_model=PredictionOut)
def predict(data: RideData):
    """
    Takes ride details and returns predicted fare using the ML model.
    """
    try:
        # Convert input data to DataFrame (because the model expects a DataFrame)
        # We use data.model_dump() for Pydantic v2, or data.dict() for v1
        input_data = {
            "PULocationID": [data.PULocationID],
            "trip_distance": [data.trip_distance],
            "hour": [data.hour],
            "day_of_week": [data.day_of_week]
        }
        features = pd.DataFrame(input_data)
        
        # Make prediction
        prediction = model.predict(features)
        
        return {
            "predicted_fare": round(float(prediction[0]), 2),
            "model_version": "v1.0-random-forest"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))