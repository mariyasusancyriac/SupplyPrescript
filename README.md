# 📦 SupplyPrescript: Closed-Loop Prescriptive Supply Chain Engine

**SupplyPrescript** is an enterprise-grade, closed-loop analytics system designed to transition supply chain operations from passive delay predictions to automated, mathematical decision prescriptions.

---

## 🏗️ System Architecture
[ Synthetic Logistics Data ] ──> [ XGBoost AI Model ] ──> Predicts Delays
│
▼
[ SciPy Optimization Engine ] ──> Prescribes 3 Solutions
│
▼
[ PostgreSQL Database ] <── [ User Decision Entry ] <── [ Interactive Dashboard ]
│
└─────────────── ( Auto-Retraining Trigger ) ───────────────┘

---

## 🛠️ Tech Stack & Domain Framework

* **Primary Language:** Python 3.10+
* **Machine Learning:** XGBoost / LightGBM (Delay Probability & Duration)
* **Optimization Engine:** SciPy (`scipy.optimize`), PuLP
* **Backend API & Write-Back:** FastAPI, SQL
* **Database Layer:** PostgreSQL
* **Frontend Visual Application:** Retool / Streamlit

---

## 📁 Repository Directory Structure

```text
SupplyPrescript/
├── database/
│   └── schema.sql         # Foundational relational schema (5 core tables)
├── data/
│   └── shipments.csv      # Synthetic supply chain shipment logs
├── scripts/
│   └── generate_data.py   # Dataset generator script
├── models/                # Machine learning models & solvers (Week 1–2)
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
