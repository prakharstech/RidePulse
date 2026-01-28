import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset
import json

# Create some dummy data with clear drift
ref_data = pd.DataFrame({
    'trip_distance': [1.5, 2.0, 3.5, 4.0, 5.5] * 20,
    'fare_amount': [10, 15, 20, 25, 30] * 20
})

# Make current data significantly different to ensure drift is detected
curr_data = pd.DataFrame({
    'trip_distance': [10.0, 15.0, 20.0, 25.0, 30.0] * 20,  # Much higher values
    'fare_amount': [100, 150, 200, 250, 300] * 20  # Much higher values
})

print("=== RUNNING REPORT WITH OBVIOUS DRIFT ===")
drift_report = Report(metrics=[DataDriftPreset()])
drift_report.run(reference_data=ref_data, current_data=curr_data)

print("\n=== EXPLORING ALL ATTRIBUTES (including private) ===")
all_attrs = dir(drift_report)
private_attrs = [a for a in all_attrs if a.startswith('_') and not a.startswith('__')]
print(f"Private attributes: {private_attrs}")

for attr in private_attrs:
    try:
        value = getattr(drift_report, attr)
        print(f"\n{attr}:")
        print(f"  Type: {type(value)}")
        
        # If it's an object with useful methods
        if hasattr(value, 'as_dict'):
            print(f"  ✓ Has as_dict() method!")
            try:
                result_dict = value.as_dict()
                print(f"    Returned type: {type(result_dict)}")
                
                if isinstance(result_dict, dict):
                    print(f"    Keys: {list(result_dict.keys())[:10]}")
                    
                    # Look for metrics
                    if 'metrics' in result_dict:
                        metrics = result_dict['metrics']
                        print(f"    Number of metrics: {len(metrics)}")
                        
                        if metrics:
                            first_metric = metrics[0]
                            print(f"    First metric keys: {list(first_metric.keys())[:15]}")
                            
                            if 'result' in first_metric:
                                result = first_metric['result']
                                print(f"\n    ✓✓✓ Found result!")
                                print(f"    Result type: {type(result)}")
                                
                                if isinstance(result, dict):
                                    print(f"    Result keys: {list(result.keys())[:15]}")
                                    
                                    if 'dataset_drift' in result:
                                        print(f"\n    ✓✓✓✓ SUCCESS! dataset_drift = {result['dataset_drift']}")
                                        print(f"\n    FULL RESULT: {json.dumps(result, indent=2)[:500]}")
                                        
            except Exception as e:
                print(f"    Error calling as_dict(): {e}")
                
    except Exception as e:
        print(f"  Error accessing: {e}")

print("\n\n=== CHECKING PRESET'S INTERNAL STRUCTURE ===")
preset = drift_report.metrics[0]
preset_private = [a for a in dir(preset) if a.startswith('_') and not a.startswith('__')]
print(f"Preset private attributes: {preset_private[:15]}")

for attr in preset_private[:10]:  # Check first 10
    try:
        value = getattr(preset, attr)
        if value is not None and not callable(value):
            print(f"\n{attr}: {type(value)}")
            
            if hasattr(value, '__dict__'):
                sub_keys = list(value.__dict__.keys())[:10]
                print(f"  Sub-keys: {sub_keys}")
                
    except Exception as e:
        pass