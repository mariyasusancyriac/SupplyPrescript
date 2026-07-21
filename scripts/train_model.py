import os
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.normpath(os.path.join(script_dir, "..", "data", "shipments.csv"))

if not os.path.exists(data_path):
    raise FileNotFoundError(f"Run generate_data.py first! Could not find {data_path}")

df = pd.read_csv(data_path)

features = ["supplier_name", "shipment_mode", "transit_path", "transit_days", "weather_score"]
X = pd.get_dummies(df[features], drop_first=True)
y = df["is_delayed"]

models_folder = os.path.normpath(os.path.join(script_dir, "..", "models"))
os.makedirs(models_folder, exist_ok=True)
joblib.dump(X.columns.tolist(), os.path.join(models_folder, "model_features.joblib"))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = XGBClassifier(
    n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("--------------------------------------------------")
print(f"📊 XGBoost Model Accuracy: {acc * 100:.2f}%")
print("--------------------------------------------------")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

model_path = os.path.join(models_folder, "xgboost_delay_model.joblib")
joblib.dump(model, model_path)
print(f"✅ Trained model saved to: {model_path}")