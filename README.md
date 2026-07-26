Here is a comprehensive, production-ready **README.md** file for your **SupplyPrescript** project. It covers everything done so far, setup/execution steps, tech stack, architecture, and team/contributor guidelines so anyone can clone and run it seamlessly.

---

#  SupplyPrescript: Closed-Loop Prescriptive Supply Chain Analytics

**SupplyPrescript** is an enterprise-grade, closed-loop prescriptive analytics system designed to transition supply chain operations from passive delay alerts to automated, mathematical decision-making.

Instead of merely warning managers that a shipment is delayed , SupplyPrescript uses machine learning to predict disruption risks , calculates optimal recovery strategies using operations research algorithms , captures operator choices via an interactive control tower , and writes those choices back to the relational database to auto-retrain prediction models over time.

---

##  System Architecture

```text
  ┌────────────────────────┐
  │  Synthetic Logistics   │
  │     Data Generation    │
  └───────────┬────────────┘
              │
              ▼
  ┌────────────────────────┐
  │  XGBoost AI Classifier │ ───► Predicts Delay Risks (ON_TIME vs DELAY_PREDICTED)
  └───────────┬────────────┘
              │
              ▼
  ┌────────────────────────┐
  │ SciPy Math Solver Engine│ ───► Prescribes 3 Budget-Constrained Options
  └───────────┬────────────┘
              │
              ▼
  ┌────────────────────────┐         ┌───────────────────────────────┐
  │   FastAPI REST Engine  │ ◄────── │ Streamlit Control Tower UI    │
  └───────────┬────────────┘         │ (Operator Action & Mutation)  │
              │                      └───────────────────────────────┘
              ▼
  ┌────────────────────────┐
  │ SQLite / DB Warehouse  │ ◄── [Write-Back Decision Logging]
  └───────────┬────────────┘
              │
              └─────────────── (Closed-Loop Retraining Trigger) ───────────────► [Auto-Model Retrainer]

```

---

##  Tech Stack & Domain Framework

* **Programming Language:** Python 3.10+ 


* **Machine Learning:** XGBoost, Scikit-Learn, Pandas, NumPy, Joblib 


* **Operations Research / Optimization:** SciPy (`scipy.optimize`), Linear Programming 


* **Backend API Framework:** FastAPI, Uvicorn, Pydantic 


* **Database & Persistence:** SQLite (`supply_chain.db`), ANSI SQL (`database/schema.sql`) 


* **Frontend Control Tower:** Streamlit 


* **Testing & Quality Assurance:** Python `unittest` / Unit Testing Suite 


* **Version Control:** Git, GitHub (Feature Branching & Pull Requests) 



---

##  Repository Directory Structure

```text
SupplyPrescript/
├── database/
│   ├── schema.sql           # Foundational 5-table relational schema definition
│   └── supply_chain.db      # Live initialized SQLite database storage
├── data/
│   └── shipments.csv        # Synthetic supply chain historical shipping dataset
├── models/
│   ├── model_features.joblib       # Saved categorical feature list
│   └── xgboost_delay_model.joblib  # Trained XGBoost classification model weights
├── scripts/
│   ├── generate_data.py     # Data generation pipeline (1,000 shipment rows)
│   ├── train_model.py       # XGBoost classifier model training script
│   ├── solver.py            # SciPy linear optimization decision engine
│   ├── app.py               # FastAPI REST service & decision endpoint
│   ├── dashboard.py         # Streamlit visual UI control tower
│   └── retrain.py           # Closed-loop automated model retraining pipeline
├── tests/
│   └── test_solver.py       # Unit tests for mathematical safety constraints
├── .gitignore               # Python version control exclusions
├── requirements.txt         # Core Python dependencies
└── README.md                # Project architecture & workflow documentation

```

---

##  Core Functionality & Work Done

### 1. Relational Database Layer (`database/schema.sql`)

Designed a 5-table relational database model with cascading constraints to support closed-loop write-back operations:

1. **Shipments:** Relational anchor for route, supplier, and transit parameters.


2. **Predictions:** Foreign-key bound landing table for XGBoost ML delay risk probabilities.


3. **Recommendations:** Holds SciPy calculated decision trade-off alternatives.


4. **Decisions:** Real-time mutation table capturing manager choices submitted through the dashboard.


5. **Results:** Logs actual arrival dates, final invoice variances, and financial ROI to trigger model auto-retraining.


### 2. Predictive Engine (`scripts/train_model.py`)

Trains an XGBoost Classifier on shipping variables (supplier, transit mode, route path, lead days, weather severity) to predict whether a shipment will arrive on time (`ON_TIME`) or be delayed (`DELAY_PREDICTED`).

### 3. Prescriptive Operations Research Engine (`scripts/solver.py`)

Triggers automatically whenever a delay is detected. SciPy solves operational trade-offs subject to a maximum budget constraint (e.g., $20,000):

* **Option A (Air Freight Expedite):** Maximum lead-time reduction (Fastest / Premium Cost).


* **Option B (Secondary Vendor Reroute):** Balanced lead-time reduction and cost.


* **Option C (Accept Delay & Reschedule):** Baseline scheduled arrival (Zero extra cost / Maximum Days).


### 4. REST API Bridge (`scripts/app.py`)

FastAPI web service serving endpoints at `http://127.0.0.1:8000`. Accepts shipment payloads, computes ML delay predictions, runs the SciPy solver on-the-fly, and exposes interactive Swagger documentation (`/docs`).

### 5. Interactive Control Tower UI (`scripts/dashboard.py`)

Streamlit dashboard built for supply chain managers to simulate shipment scenarios, view prescribed mitigation options, and write decisions directly back into the live SQLite database.

### 6. Closed-Loop Auto-Retrainer & Safety Suite (`scripts/retrain.py`, `tests/test_solver.py`)

* Includes automated unit tests verifying that solver equations never violate cost thresholds or output invalid metrics.


* Implements a closed-loop trigger script that reads human choices and final invoice data to retrain the XGBoost baseline.



---

##  How to Run the System (Step-by-Step for Contributors)

To run the complete system locally, open **3 separate terminal tabs** in Visual Studio Code:

### Prerequisites & Installation

Clone the repository and install all required Python packages:

```bash
git clone https://github.com/mariyasusancyriac/SupplyPrescript.git
cd SupplyPrescript
py -m pip install pandas numpy scikit-learn xgboost scipy fastapi uvicorn pydantic streamlit requests joblib

```

---

###  Terminal Tab #1: Start the Backend API Engine

1. Open VS Code Terminal (Ctrl + `).


2. Navigate into the `scripts/` directory:


```bash
cd scripts

```


3. Start the FastAPI server:


```bash
py -m uvicorn app:app --reload

```


* The server will launch at `http://127.0.0.1:8000`. Keep this terminal tab running in the background! 





---

### 📍 Terminal Tab #2: Start the Streamlit Control Tower UI

1. Open a **2nd terminal tab** (click the `+` icon in the terminal panel).


2. Navigate into `scripts/`:


```bash
cd scripts

```


3. Launch the web dashboard:


```bash
py -m streamlit run dashboard.py

```


* Your web browser will automatically open the control panel at `http://localhost:8501`.





---

### 📍 Terminal Tab #3: Run Unit Tests & Retraining Pipeline

Open a **3rd terminal tab** at the root project directory to run safety checks or model retraining whenever needed:

* **Run Mathematical Safety Unit Tests:**
```bash
py tests/test_solver.py

```



(Verifies that optimization equations never violate hard business logic or return invalid costs).


* **Trigger Closed-Loop Model Retraining:**
```bash
py scripts/retrain.py

```



(Feeds real manager choices and results back into XGBoost to retrain model weights).



---

## 👥 Members & Contributors

* **Mariya Susan Cyriac** — Data Analyst Intern


* **Jaswanth** — Data Analyst Intern


* **Sekhar** — Data Analyst Intern



---

## 📄 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).
