"""
Main 'body':
- Running this file only is enough, there's no need to run the other files individually.
"""
from one_calc_weights import weights_optimisation
from two_forecast_generation import generate_forecast
from three_weekly_plan_creation import weekly_plan

if __name__ == "__main__":
    weights_optimisation()
    generate_forecast()
    weekly_plan()