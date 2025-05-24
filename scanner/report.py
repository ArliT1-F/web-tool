import os
import json

def save_scan_report(data, filename):
    os.makedirs("reports", exist_ok=True)
    with open(os.path.join("reports", filename), "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved to reports/{filename}")