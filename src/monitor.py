import pandas as pd
from scipy import stats
import json
import os
from dotenv import load_dotenv
import requests 
load_dotenv()


# CONFIG
REFERENCE_DATA_PATH = "./data/raw/jan_data.csv"
CURRENT_DATA_PATH = "./data/raw/feb_data.csv"

# --- GITHUB CONFIGURATION ---
# 1. Enter your GitHub Username
GITHUB_USER = "prakharstech"  
# 2. Enter the Repo Name (e.g., RidePulse)
GITHUB_REPO = "RidePulse"
# 3. Enter your Personal Access Token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def trigger_retraining():
    print("🚀 Initiating Cloud Retraining Pipeline...")
    
    if "YOUR_GITHUB" in GITHUB_TOKEN:
        print("⚠️  Simulated Trigger (No Token detected). skipping API call.")
        print("    (To actually run GitHub Actions, paste your Token in the script)")
        return

    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "event_type": "retrain_model_event",
        "client_payload": {"reason": "drift_detected_by_ks_test"}
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 204:
            print("✅ Signal sent! GitHub Actions is now retraining the model.")
        else:
            print(f"❌ Failed to trigger GitHub: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def detect_drift():
    print("🔎 Loading data for drift analysis...")
    reference = pd.read_csv(REFERENCE_DATA_PATH)
    current = pd.read_csv(CURRENT_DATA_PATH)
    
    # --- CHAOS MODE: SIMULATE DRIFT ---
    print("😈 CHAOS MODE: Artificially inflating Feb fares by 50%...")
    current['fare_amount'] = current['fare_amount'] * 1.5
    # ----------------------------------
    
    columns_to_monitor = ['trip_distance', 'fare_amount']
    print(f"📊 Comparing Jan vs Feb (Modified)...")
    
    drift_detected = False
    
    for col in columns_to_monitor:
        ref_values = reference[col].dropna()
        curr_values = current[col].dropna()
        
        # KS Test
        statistic, pvalue = stats.ks_2samp(ref_values, curr_values)
        
        # If p-value is tiny (near 0), the distributions are different
        is_drift = pvalue < 0.05
        status = "🔴 DRIFT" if is_drift else "🟢 OK"
        
        print(f"  {col:20} | p-value: {pvalue:.10f} | {status}")
        
        if is_drift:
            drift_detected = True

    print("\n" + "=" * 50)
    
    if drift_detected:
        print("🔴 DRIFT DETECTED! The data has changed significantly.")
        print("   -> Action: Triggering automated retraining...")
        trigger_retraining()
        return True
    else:
        print("🟢 System Healthy. No drift detected.")
        return False

if __name__ == "__main__":
    detect_drift()