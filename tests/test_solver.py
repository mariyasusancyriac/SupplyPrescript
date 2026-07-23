import sys
import os

# Add scripts directory to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from solver import calculate_prescriptions

def test_solver_returns_three_options():
    # Pass argument positionally so it works regardless of param name
    prescriptions = calculate_prescriptions(25)
    assert len(prescriptions) == 3, "Solver should return exactly 3 mitigation paths."

def test_air_freight_reduces_days():
    prescriptions = calculate_prescriptions(25)
    air_freight = prescriptions[0]
    assert air_freight["days_saved"] > 0, "Air Freight must reduce transit time."
    assert air_freight["final_transit_days"] < 25, "Final transit days must be less than original."

def test_costs_are_positive():
    prescriptions = calculate_prescriptions(20)
    for p in prescriptions:
        assert p["cost"] >= 0, "Prescription cost cannot be negative."

if __name__ == "__main__":
    test_solver_returns_three_options()
    test_air_freight_reduces_days()
    test_costs_are_positive()
    print("✅ All unit tests passed successfully!")