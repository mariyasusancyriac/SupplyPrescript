import os
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

num_samples = 1000

suppliers = ['Supplier_A', 'Supplier_B', 'Supplier_C', 'Supplier_D']
modes = ['Sea', 'Air', 'Rail', 'Truck']
paths = ['Path_1', 'Path_2', 'Path_3', 'Path_4']

data = {
    'supplier_name': np.random.choice(suppliers, num_samples),
    'shipment_mode': np.random.choice(modes, num_samples),
    'transit_path': np.random.choice(paths, num_samples),
    'transit_days': np.random.randint(5, 45, num_samples),
    'weather_score': np.random.randint(1, 11, num_samples),
}

df = pd.DataFrame(data)

# Clear mathematical rule: High weather score (>=7) OR high transit days (>=28) = DELAY (1)
df['is_delayed'] = np.where((df['weather_score'] >= 7) | (df['transit_days'] >= 28), 1, 0)

# Save to data directory
output_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(output_dir, exist_ok=True)
df.to_csv(os.path.join(output_dir, "shipments.csv"), index=False)

print("✅ New datasets generated with clear delay patterns in data/shipments.csv!")