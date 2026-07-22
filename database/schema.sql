-- SupplyPrescript Relational Database Schema

-- 1. Shipments Table: Logs baseline shipment lanes and parameters
CREATE TABLE IF NOT EXISTS Shipments (
    shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name VARCHAR(50) NOT NULL,
    shipment_mode VARCHAR(20) NOT NULL,
    transit_path VARCHAR(50) NOT NULL,
    scheduled_days INT NOT NULL,
    weather_score INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Predictions Table: Stores Machine Learning output probabilities
CREATE TABLE IF NOT EXISTS Predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INT REFERENCES Shipments(shipment_id),
    is_delayed INT NOT NULL, -- 1 = Delayed, 0 = On Time
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Recommendations Table: Stores SciPy solved trade-off options
CREATE TABLE IF NOT EXISTS Recommendations (
    recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id INT REFERENCES Predictions(prediction_id),
    option_name VARCHAR(50) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    days_saved INT NOT NULL,
    final_transit_days INT NOT NULL
);

-- 4. Decisions Table: Captures user selections from the dashboard
CREATE TABLE IF NOT EXISTS Decisions (
    decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INT REFERENCES Shipments(shipment_id),
    selected_option VARCHAR(50) NOT NULL,
    decision_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Results Table: Logs actual operational outcomes for dynamic model retraining
CREATE TABLE IF NOT EXISTS Results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INT REFERENCES Shipments(shipment_id),
    actual_days INT NOT NULL,
    final_cost DECIMAL(10, 2) NOT NULL,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);