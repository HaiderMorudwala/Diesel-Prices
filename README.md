# Diesel-Prices
#Trucker Diesel & Route Optimizer

A Python-based logistics tool that calculates the Total Cost of Ownership (TCO) for refueling stops. Instead of just finding the lowest price, this engine factors in "detour mileage, fuel burn, and the monetary value of time lost in traffic".

Key Features
Massive Data Simulation: Generates a database of 50,000 fuel stations clustered around 500 highway exits.
Route-Aware Logic: Uses **Manhattan Distance** to calculate the exact "extra miles" added to a trip.
Safety & Traffic Check: Implements a "Traffic Tax"—automatically deprioritizing stations in high-congestion areas by converting minutes of delay into dollar costs ($75/hr).
Persistent Trip Log: Saves every search to a local `trip_plan.txt` without overwriting previous history, creating a long-term "black box" for fuel expenses.

How it Works
The optimizer calculates the "Net Savings" using the following logic:
Net Savings = (Current Price \times Gallons) - (Station Price \times Gallons + Detour Fuel Cost + Traffic Time Cost)
If the result is positive, the stop is profitable. If negative, the driver is advised to "Stay Put."

 Installation & Usage
1.  Clone the Repo:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    ```
2.  Install Dependencies:
    ```bash
    pip install pandas numpy
    ```
3.  Run the Engine:
    ```bash
    python main.py
    ```
Example Output

STATION NAME         | PRICE  | EXTRA MILES  | TRAFFIC    | NET SAVINGS
-------------------------------------------------------------------------
Exit_290_Station_18  | $3.38  | 0.0          | ✅ CLEAR   | $64.31
Exit_290_Station_29  | $3.38  | 0.2          | ✅ CLEAR   | $63.85
...

Technologies Used
Python 3.x
Pandas: Data manipulation and analysis.
NumPy: Mathematical computations.
UTF-8 Encoding: For universal character support in log files.

Created by Haider Mohammed Morudwala
