import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from solver import calculate_prescriptions

app = FastAPI(
    title="SupplyPrescript API",
    description="Prescriptive Analytics API for Supply Chain Delay Resolution",
    version="1.0"
)

# Dynamically locate saved model and feature artifacts
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.normpath(os.path.join(script_dir, "..", "models", "xgboost_delay_model.joblib"))
features_path = os.path.normpath(os.path.join(script_dir, "..", "models", "model_features.joblib"))

# Load trained artifacts
if os.path.exists(model_path) and os.path.exists(features_path):
    model = joblib.load(model_path)
    model_features = joblib.load(features_path)
else:
    model, model_features = None, None


class ShipmentInput(BaseModel):
    supplier_name: str
    shipment_mode: str
    transit_path: str
    transit_days: int
    weather_score: int


@app.get("/")
def home():
    return {
        "status": "Online",
        "message": "Welcome to the SupplyPrescript API engine!"
    }


@app.post("/predict-and-prescribe")
def predict_and_prescribe(data: ShipmentInput):
    if model is None or model_features is None:
        raise HTTPException(
            status_code=500,
            detail="Model files not found. Ensure train_model.py has been executed."
        )

    # 1. Prepare raw input data
    input_dict = data.model_dump()
    df_input = pd.DataFrame([input_dict])

    # 2. Convert categories to One-Hot Encoding
    df_encoded = pd.get_dummies(df_input)

    # 3. Align columns strictly with the ML training layout
    df_reindexed = df_encoded.reindex(columns=model_features, fill_value=0)

    # 4. Predict Delay (1 = Delayed, 0 = On Time)
    prediction = int(model.predict(df_reindexed)[0])

    # 5. Calculate prescriptive trade-off options if a delay is predicted
    prescriptions = []
    if prediction == 1:
        prescriptions = calculate_prescriptions(data.transit_days)

    return {
        "prediction": prediction,
        "delay_status": "DELAY_PREDICTED" if prediction == 1 else "ON_TIME",
        "prescriptions": prescriptions
    }