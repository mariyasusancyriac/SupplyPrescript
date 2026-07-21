import os
import joblib
import numpy as np

def calculate_prescriptions(transit_days, base_cost=5000, max_budget=20000):
    """
    Computes 3 optimized operational solutions for delayed shipments.
    """
    # Solution 1: Air Freight (Cuts transit days by 70%, increases cost)
    air_cost = base_cost + (transit_days * 350)
    air_days = max(1, int(transit_days * 0.3))

    # Solution 2: Secondary Vendor (Cuts transit days by 40%, moderate cost)
    vendor_cost = base_cost + (transit_days * 180)
    vendor_days = max(2, int(transit_days * 0.6))

    # Solution 3: Launch Delay (No change in speed, zero extra cost)
    launch_delay_cost = base_cost
    launch_delay_days = transit_days

    solutions = [
        {
            "option": "Option A: Air Freight Expedite",
            "cost": round(air_cost, 2),
            "days_saved": transit_days - air_days,
            "final_transit_days": air_days,
            "within_budget": air_cost <= max_budget
        },
        {
            "option": "Option B: Reroute to Secondary Vendor",
            "cost": round(vendor_cost, 2),
            "days_saved": transit_days - vendor_days,
            "final_transit_days": vendor_days,
            "within_budget": vendor_cost <= max_budget
        },
        {
            "option": "Option C: Accept Delay & Reschedule",
            "cost": round(launch_delay_cost, 2),
            "days_saved": 0,
            "final_transit_days": launch_delay_days,
            "within_budget": True
        }
    ]
    return solutions


if __name__ == "__main__":
    # Test solver on a delayed shipment taking 25 days
    sample_transit_days = 25
    print(f"🔍 Calculating Solved Options for a {sample_transit_days}-day delay...")
    print("------------------------------------------------------------------")
    
    results = calculate_prescriptions(sample_transit_days)
    for opt in results:
        print(f"📌 {opt['option']}")
        print(f"   - Total Cost: ${opt['cost']}")
        print(f"   - Final Transit Days: {opt['final_transit_days']} days (Saved {opt['days_saved']} days)")
        print(f"   - Within Budget: {opt['within_budget']}\n")