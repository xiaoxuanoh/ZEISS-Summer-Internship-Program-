"""
This is the second file.

Purpose:
- Produce monthly forecast using the optimised weights from one_calc_weights.py.

The csv file used for this code:
- current_month_data.csv: 
    -The data in this file contains forecasts from SAP and S&OP orders received for the current month.
- calculated_weights.csv:
    -Obtained from one_calc_weights.py, contains the optimized weights (alpha and beta).

Output:
- current_month_forecast.csv:
    -The column "forecast_by_weights" contains forecasted production quantities according to the optimised weights.
"""
import pandas as pd

def generate_forecast(input_data="/Users/xxoh/Documents/weekly production planner/csv files/current_month_data.csv",
                      weight_file="/Users/xxoh/Documents/weekly production planner/csv files/calculated_weights.csv",
                      output_path="/Users/xxoh/Documents/weekly production planner/csv files/current_month_forecast.csv"):
    df = pd.read_csv(input_data)
    weights_df = pd.read_csv(weight_file)
    weights = dict(zip(weights_df["weight_name"], weights_df["value"]))

    df["forecast_by_weights"] = df["sap_forecast"] * weights["alpha"] + df["sop_orders_received"] * weights["beta"]
    df["forecast_by_weights"] = df["forecast_by_weights"].round(0).astype(int)
    df.to_csv(output_path, index=False)
    print(f"Monthly forecast saved to {output_path}")

if __name__ == "__main__":
    generate_forecast()