import os
import random
import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)

NUM_SAMPLES = 1000

suppliers = ["Apex Logistics", "Global Freight Co", "Pacific Line", "Nordic Carriers", "Atlas Supply"]
modes = ["Ocean", "Air Freight", "Rail", "Trucking"]
transit_paths = ["Asia-US_West", "Europe-US_East", "Asia-Europe", "US_Domestic", "LatAm-US_Gulf"]

data = []

for i in range(1, NUM_SAMPLES + 1):
    shipment_id = i
    supplier = random.choice(suppliers)
    mode = random.choice(modes)
    path = random.choice(transit_paths)

    if mode == "Air Freight":
        transit_days = random.randint(2, 5)
    elif mode == "Trucking":
        transit_days = random.randint(3, 7)
    elif mode == "Rail":
        transit_days = random.randint(7, 14)
    else:
        transit_days = random.randint(15, 35)

    weather_score = random.randint(1, 10)

    delay_prob = 0.15
    if weather_score < 4:
        delay_prob += 0.35
    if transit_days > 20:
        delay_prob += 0.25

    is_delayed = 1 if random.random() < delay_prob else 0

    data.append({
        "shipment_id": shipment_id,
        "supplier_name": supplier,
        "shipment_mode": mode,
        "transit_path": path,
        "transit_days": transit_days,
        "weather_score": weather_score,
        "is_delayed": is_delayed
    })

df = pd.DataFrame(data)

script_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.normpath(os.path.join(script_dir, "..", "data"))
os.makedirs(folder_path, exist_ok=True)
output_path = os.path.join(folder_path, "shipments.csv")

df.to_csv(output_path, index=False)

print(f"✅ Success! Generated {NUM_SAMPLES} shipment records at: {output_path}")
print(df.head())