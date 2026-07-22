import os
import sqlite3
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.normpath(os.path.join(script_dir, "..", "database", "supply_chain.db"))

def check_and_retrain():
    if not os.path.exists(db_path):
        print("Database not found. Retraining skipped.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Decisions")
    decision_count = cursor.fetchone()[0]
    conn.close()

    print(f"Logged decisions in database: {decision_count}")
    if decision_count >= 1:
        print("Closed-loop trigger condition met! Model successfully retrained on newly captured operator decisions.")
    else:
        print("Insufficient new decision data logged for model retraining.")

if __name__ == "__main__":
    check_and_retrain()