# 📦 SupplyPrescript: Closed-Loop Prescriptive Supply Chain Engine

**SupplyPrescript** is an enterprise-grade, closed-loop prescriptive analytics platform that transitions supply chain management from passive delay predictions to automated, mathematical decision optimization.

---

## 🏗️ Closed-Loop System Architecture

```text
[ 1. Data Generator ] ──► Generates 1,000 Historical Shipment Records (shipments.csv)
                                   │
                                   ▼
[ 2. Predictive AI Engine ] ──► XGBoost ML Model Predicts Delay Risks (train_model.py)
                                   │
                                   ▼ (If Delay Predicted)
[ 3. Prescriptive Engine ] ──► SciPy Optimization Engine Solves Trade-Off Options (solver.py)
                                   │
                                   ▼
[ 4. Web REST Backend ]    ──► FastAPI / Uvicorn API Engine Serves Endpoint (app.py)
                                   │
                                   ▼
[ 5. Relational Database ] ──► SQLite Database Stores System State (supply_chain.db)

##🛠️ Tech Stack & Implementation Details
-[x] Language: Python 3.10+

-[x] Machine Learning: XGBoost, Scikit-Learn, Joblib, Pandas

-[x] Operations Research / Optimization: SciPy (scipy.optimize)

-[x] REST API Service: FastAPI, Uvicorn, Pydantic

-[x] Database Layer: SQLite (supply_chain.db) initialized via ANSI SQL (schema.sql)

-[x] Frontend Visualization: Streamlit (Control Tower UI)

-[x] Version Control: Git & GitHub

##📁 Repository Directory Structure

SupplyPrescript/
├── database/
│   ├── schema.sql                   # 5 relational table definitions (Shipments, Predictions, etc.)
│   └── supply_chain.db              # Active initialized SQLite database engine
├── data/
│   └── shipments.csv                # 1,000 historical shipping records dataset
├── models/
│   ├── xgboost_delay_model.joblib   # Serialized XGBoost delay classification model
│   └── model_features.joblib        # Preprocessed One-Hot Encoding feature layout
├── scripts/
│   ├── generate_data.py             # Synthetic supply chain data generation pipeline
│   ├── train_model.py               # XGBoost model training and evaluation script
│   ├── solver.py                    # SciPy prescriptive optimization engine
│   └── app.py                       # FastAPI REST API serving live delay & solver endpoint
└── README.md                        # Primary project documentation

##📊 Core Functional Workflow
1. Database Initialization
database/schema.sql defines five interconnected tables supporting bidirectional data loops:

    Shipments: Baseline lane logs & shipment parameters.

    Predictions: Machine learning probability outputs.

    Recommendations: SciPy solved trade-off operational paths.

    Decisions: User dashboard choices.

    Results: Real-world lead-time and invoice records for continuous retraining.

2. Predictive & Prescriptive Pipeline
When a shipment is processed via the FastAPI backend (POST /predict-and-prescribe):

    1. Predictive Engine (train_model.py): Evaluates transit days, shipment modes, suppliers, and weather severity scores to classify whether the shipment is ON_TIME (0) or DELAY_PREDICTED (1).
    2. Prescriptive Engine (solver.py): If a delay is detected, SciPy computes 3 solved mitigation paths subject to operational cost and time constraints:
        Option A (Air Freight Expedite): Maximum time saved (Fastest / Premium Cost).
        Option B (Secondary Vendor Reroute): Balanced cost and lead-time mitigation.
        Option C (Accept Delay & Reschedule): Baseline scheduled arrival (Lowest Cost / Maximum Lead Time).

##🚀 How to Run the Project Locally
    1. Initialize the SQLite Database
        py -c "import sqlite3; conn = sqlite3.connect('database/supply_chain.db'); conn.executescript(open('database/schema.sql').read()); conn.close()"
    2. Launch the FastAPI Backend Server
        cd scripts
        py -m uvicorn app:app --reload
        -[x] API Documentation (Swagger UI): Open browser at http://127.0.0.1:8000/docs