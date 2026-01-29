import pandas as pd
import numpy as np
import random
from datetime import datetime

# --- 1. DATA GENERATION ---
def create_dataset():
    stations = []
    exits = [(random.uniform(0, 500), random.uniform(0, 500)) for _ in range(500)]
    for i, (exit_x, exit_y) in enumerate(exits):
        base_price = random.uniform(3.40, 4.40)
        traffic_delay_min = random.uniform(0, 30) 
        for s in range(100):
            stations.append({
                "station_name": f"Exit_{i}_Station_{s}",
                "diesel_price": round(base_price + random.uniform(-0.05, 0.05), 2),
                "x_coord": exit_x + random.uniform(-0.5, 0.5),
                "y_coord": exit_y + random.uniform(-0.5, 0.5),
                "traffic_delay": traffic_delay_min
            })
    pd.DataFrame(stations).to_csv("diesel_prices_large.csv", index=False)

# --- 2. THE ENGINE ---
def find_best_deal(local_p, needed_gal, mpg, s_x, s_y, d_x, d_y):
    df = pd.read_csv("diesel_prices_large.csv")
    DRIVER_TIME_VAL = 75.00
    direct_trip_miles = abs(s_x - d_x) + abs(s_y - d_y)
    
    df['dist_to_station'] = abs(s_x - df['x_coord']) + abs(s_y - df['y_coord'])
    df['dist_to_dest'] = abs(df['x_coord'] - d_x) + abs(df['y_coord'] - d_y)
    df['extra_miles'] = (df['dist_to_station'] + df['dist_to_dest'] - direct_trip_miles).clip(lower=0)
    
    df['detour_fuel_cost'] = (df['extra_miles'] / mpg) * df['diesel_price']
    df['traffic_time_cost'] = (df['traffic_delay'] / 60) * DRIVER_TIME_VAL
    df['total_potential_cost'] = (needed_gal * df['diesel_price']) + df['detour_fuel_cost'] + df['traffic_time_cost']
    
    df['net_savings'] = (local_p * needed_gal) - df['total_potential_cost']
    return df.sort_values(by='net_savings', ascending=False).head(5)

# --- 3. NEW: THE LOGGING FEATURE ---
def save_results_to_file(results, start, end, final_savings):
    filename = "trip_plan.txt"
    # Mode "a" stands for APPEND. It adds to the file instead of overwriting.
    with open(filename, "a", encoding="utf-8") as f:
        f.write("\n" + "#" * 65 + "\n") # Large separator for new entries
        f.write(f"NEW TRIP SEARCH: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("#" * 65 + "\n")
        
        f.write(f"ROUTE: {start} → {end}\n")
        f.write(f"POTENTIAL SAVINGS: ${round(final_savings, 2)}\n\n")
        
        f.write(f"{'STATION':<20} | {'PRICE':<7} | {'EXTRA MILES':<12} | {'NET SAVINGS'}\n")
        f.write("-" * 65 + "\n")
        
        for _, row in results.iterrows():
            f.write(f"{row['station_name']:<20} | ${row['diesel_price']:<6} | {round(row['extra_miles'], 1):<12} | ${round(row['net_savings'], 2)}\n")
        
        f.write("\nDECISION: " + ("STOP AND REFUEL" if final_savings > 0 else "KEEP DRIVING - NO PROFITABLE STOPS") + "\n")
        f.write("=" * 65 + "\n\n")

    print(f"✅ Entry added to your persistent log: '{filename}'")
# --- 4. RUN ---
if __name__ == "__main__":
    create_dataset()
    print("--- INPUT DATA ---")
    lp = float(input("Local Price: "))
    g = float(input("Gallons: "))
    m = float(input("MPG: "))
    sx, sy = float(input("Start X: ")), float(input("Start Y: "))
    dx, dy = float(input("Dest X: ")), float(input("Dest Y: "))
    
    top_results = find_best_deal(lp, g, m, sx, sy, dx, dy)
    
    # Print Table
    print("\n" + top_results[['station_name', 'diesel_price', 'extra_miles', 'net_savings']].to_string())
    print("\nACTION: Use the station in the first row. It offers the highest net profit after fuel and time costs.")
    
    # Save to file
    save_results_to_file(top_results, (sx, sy), (dx, dy), top_results.iloc[0]['net_savings'])