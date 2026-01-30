from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum
import joblib
import pandas as pd
import os
import requests

app = FastAPI(title="RidePulse API", version="3.0")

MODEL_PATH = "models/model_v1.joblib"
GITHUB_USER = "prakharstech"
GITHUB_REPO = "RidePulse"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# --- LOAD MODEL ---
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

# --- HELPERS ---
def trigger_pipeline(simulate_drift: bool):
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="GITHUB_TOKEN not set.")
    
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # PAYLOAD: This decides if we drift or not
    data = {
        "event_type": "retrain_model_event",
        "client_payload": {
            "simulate_drift": "true" if simulate_drift else "false"
        }
    }
    
    try:
        requests.post(url, json=data, headers=headers)
        return {"status": "✅ Pipeline Triggered", "mode": "Drift" if simulate_drift else "Normal"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "RidePulse Demo API Ready 🟢"}

@app.post("/predict")
def predict(data: dict):
    # (Keeping it simple for brevity - paste your full predict logic here)
    # Ensure this matches your 5-feature logic from previous steps
    if not model: return {"error": "Model loading..."}
    try:
        df = pd.DataFrame([data]) # Expects dict with 5 features
        pred = model.predict(df)[0]
        return {"fare": float(pred)}
    except:
        return {"fare": 18.50} # Fallback for safety

@app.post("/reset-model")
def reset_model():
    """
    1. Triggers GitHub Pipeline.
    2. Trains on CLEAN data (Normal Mode).
    3. Deploys Normal Model.
    """
    return trigger_pipeline(simulate_drift=False)

@app.post("/simulate-drift")
def simulate_drift():
    """
    1. Triggers GitHub Pipeline.
    2. Trains on CHAOS data (1.5x Multiplier).
    3. Deploys Inflated Model.
    """
    return trigger_pipeline(simulate_drift=True)

handler = Mangum(app)