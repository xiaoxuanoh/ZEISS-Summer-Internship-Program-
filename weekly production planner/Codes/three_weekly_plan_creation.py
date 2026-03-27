"""
This is the third file.

Purpose:
- Create the weekly production plan, based on the forecast, and export it into an Excel file with a specific format.

csv files used for this code:
- current_month_forecast.csv

Output:
- weekly_plan.xlsx
"""
import pandas as pd

def weekly_plan(input_file="/Users/xxoh/Documents/weekly production planner/csv files/current_month_forecast.csv",
                output_path="/Users/xxoh/Documents/weekly production planner/csv files/weekly_plan.xlsx",
                month="2025-8"):
    df = pd.read_csv(input_file)

    calendar = pd.date_range(start=f"{month}-01", end=f"{month}-30", freq="D")
    calendar_df = pd.DataFrame({
        "Date": calendar,
        "Day": calendar.day_name(),
        "Label": calendar.day_name().str[:3] + " " + calendar.day.astype(str),
        "SortOrder": calendar.dayofweek
    })

    calendar_df = calendar_df.sort_values(["Date"]).reset_index(drop=True)
    weekdays = calendar_df[calendar_df["Day"].isin(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])]
    weekends = calendar_df[~calendar_df["Day"].isin(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])]
    plan_df = pd.DataFrame({"Date": weekdays["Label"].tolist()})

    for _, row in df.iterrows():
        forecast = row["forecast_by_weights"]
        sku = row["material_number"]
        base = forecast // len(weekdays)
        remainder = forecast % len(weekdays)
        daily = [base] * len(weekdays)
        for i in range(remainder):
            daily[i] += 1
        plan_df[sku] = daily

    for _, row in weekends.iterrows():
        empty_row = pd.DataFrame([[row["Label"]] + [None]*(len(df))], columns=plan_df.columns)
        plan_df = pd.concat([plan_df, empty_row], ignore_index=True)

    # Sort plan_df by original date order
    plan_df["_sort"] = plan_df["Date"].apply(lambda x: int(x.split(" ")[1]) if isinstance(x, str) and x.split(" ")[1].isdigit() else 0)
    plan_df = plan_df.sort_values(by="_sort").drop(columns="_sort")

    component_names = df["product_name"].tolist()
    forecast_values = df["forecast_by_weights"].tolist()
    material_numbers = df["material_number"].tolist()

    header_row = pd.DataFrame([[
        f"Production Plan for {month}"] + [""] * len(material_numbers)], columns=["Date"] + material_numbers)
    component_row = pd.DataFrame([[
        "Component name"] + component_names], columns=["Date"] + material_numbers)
    total_row = pd.DataFrame([[
        "Total required"] + forecast_values], columns=["Date"] + material_numbers)
    total_units_row = pd.DataFrame([[
        "Total units"] + [int(plan_df[col].sum(skipna=True)) for col in material_numbers]], columns=["Date"] + material_numbers)

    combined = pd.concat([header_row, total_row, plan_df, total_units_row], ignore_index=True)
    combined["Total working hours"] = ""
    combined["According to plan (Y/N)"] = ""

    with pd.ExcelWriter(output_path) as writer:
        combined.to_excel(writer, sheet_name="T1 weekly planning", index=False)

    print(f"Weekly plan and Excel file saved to {output_path}")

if __name__ == "__main__":
    weekly_plan()