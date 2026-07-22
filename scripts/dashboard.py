import os
import sqlite3
import requests
import streamlit as st

st.set_page_config(page_title="SupplyPrescript Control Tower", layout="wide")

st.title("📦 SupplyPrescript: Prescriptive Supply Chain Control Tower")
st.markdown("Predict shipment delays, generate optimized resolutions, and log operational decisions.")

# Locate SQLite database safely
db_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "database", "supply_chain.db"))

def save_decision_to_db(supplier_name, shipment_mode, transit_path, scheduled_days, weather_score, selected_option):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Log shipment row
    cursor.execute("""
        INSERT INTO Shipments (supplier_name, shipment_mode, transit_path, scheduled_days, weather_score)
        VALUES (?, ?, ?, ?, ?)
    """, (supplier_name, shipment_mode, transit_path, scheduled_days, weather_score))
    shipment_id = cursor.lastrowid
    
    # 2. Log closed-loop manager decision
    cursor.execute("""
        INSERT INTO Decisions (shipment_id, selected_option)
        VALUES (?, ?)
    """, (shipment_id, selected_option))
    
    conn.commit()
    conn.close()

# Sidebar User Inputs
st.sidebar.header("Shipment Parameters")
supplier_name = st.sidebar.selectbox("Supplier Name", ["Supplier_A", "Supplier_B", "Supplier_C", "Supplier_D"])
shipment_mode = st.sidebar.selectbox("Shipment Mode", ["Sea", "Air", "Rail", "Truck"])
transit_path = st.sidebar.selectbox("Transit Path", ["Path_1", "Path_2", "Path_3", "Path_4"])
transit_days = st.sidebar.number_input("Scheduled Transit Days", min_value=1, max_value=60, value=30)
weather_score = st.sidebar.slider("Weather Severity Score (1-10)", min_value=1, max_value=10, value=8)

# Run Analysis
if st.sidebar.button("Analyze Shipment"):
    payload = {
        "supplier_name": supplier_name,
        "shipment_mode": shipment_mode,
        "transit_path": transit_path,
        "transit_days": transit_days,
        "weather_score": weather_score
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict-and-prescribe", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            st.subheader("1. AI Delay Prediction")
            if data["prediction"] == 1:
                st.error("⚠️ DELAY PREDICTED! Action Required.")
            else:
                st.success("✅ SHIPMENT ON TIME! No action required.")

            if data["prescriptions"]:
                st.subheader("2. Mathematically Solved Operational Options")
                
                cols = st.columns(len(data["prescriptions"]))
                for idx, opt in enumerate(data["prescriptions"]):
                    with cols[idx]:
                        st.metric(label=opt["option"], value=f"${opt['cost']:,}")
                        st.write(f"⏱️ **Final Transit Days:** {opt['final_transit_days']} days")
                        st.write(f"⚡ **Days Saved:** {opt['days_saved']} days")
                        st.write(f"💰 **Within Budget:** {opt['within_budget']}")
                        
                        if st.button(f"Select Option {chr(65+idx)}", key=f"btn_{idx}"):
                            save_decision_to_db(supplier_name, shipment_mode, transit_path, transit_days, weather_score, opt['option'])
                            st.success(f"Recorded selection into database: {opt['option']}")
        else:
            st.error(f"Backend Server Error: {response.status_code}")

    except Exception as e:
        st.error(f"Could not connect to API server at http://127.0.0.1:8000. Start app.py first! Error: {e}")

# Database Audit Section
st.markdown("---")
st.subheader("3. Database Decision Audit Log (`supply_chain.db`)")
if st.button("Refresh Database Log"):
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.decision_id, s.supplier_name, s.shipment_mode, s.weather_score, d.selected_option, d.decision_timestamp
            FROM Decisions d
            JOIN Shipments s ON d.shipment_id = s.shipment_id
            ORDER BY d.decision_id DESC
        """)
        records = cursor.fetchall()
        conn.close()
        
        if records:
            st.table(records)
        else:
            st.info("No manager decisions logged in the database yet.")
    else:
        st.warning("Database file not found.")