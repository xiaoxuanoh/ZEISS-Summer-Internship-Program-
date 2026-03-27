"""
This is the first file.

The following code is used to calculate the optimised weights for the forecasting model using linear programming.
The csv file created from this code will be used to generate the forecast for the next month.

The csv file used for this code:
- prev_month_forecast.csv: 
    -The data in this file should contain forecasts and actual production data from the previous month.

Output:
- calculated_weights.csv: 
    - This file contains the optimised weights (alpha and beta) for the forecasting model.
"""
import pandas as pd
import csv
from pulp import LpProblem, LpVariable, lpSum, LpMinimize
def weights_optimisation(input_path='/Users/xxoh/Documents/weekly production planner/csv files/prev_month_forecast.csv',
                        output_path='/Users/xxoh/Documents/weekly production planner/csv files/calculated_weights.csv'):
    df = pd.read_csv(input_path)
    n = len(df)

    alpha = LpVariable("alpha", lowBound=0)
    beta = LpVariable("beta", lowBound=0)
    errors = [LpVariable(f"e_{i}", lowBound=0) for i in range(n)]

    model = LpProblem("MinimizeAbsoluteError", LpMinimize)
    model += lpSum(errors)
    model += alpha + beta == 1

    for i in range(n):
        pred = alpha * df.loc[i, "sap_forecast"] + beta * df.loc[i, "sop_orders_received"]
        actual = df.loc[i, "actual_produced"]
        model += pred - actual <= errors[i]
        model += pred - actual >= -errors[i]

    model.solve()

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["weight_name", "value"])
        writer.writerow(["alpha", round(alpha.varValue, 4)])
        writer.writerow(["beta", round(beta.varValue, 4)])
        
    print(f"Optimal weights are saved to {output_path}")

if __name__ == "__main__":
    weights_optimisation()
