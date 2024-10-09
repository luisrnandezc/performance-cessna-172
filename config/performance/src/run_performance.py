"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023
"""

import os
import sys
from . import input_check
from . import data
from . import wind
from . import takeoff
from . import cruise
from . import fuel
from . import landing
import pandas as pd

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


def compute_performance(input_data):

    # TODO: Extract data for cleaning.

    # Check input data.
    input_data = input_check.check_input_data(input_data)

    # Store performance data.
    performance_path = r'C:\Users\luish\Desktop\Projects\performance_cessna_172\config\performance\src\data'
    takeoff_df = pd.read_csv(performance_path + '\\' + 'takeoff.csv')
    roc_df = pd.read_csv(performance_path + '\\' + 'roc.csv', index_col=0)
    climb_df = pd.read_csv(performance_path + '\\' + 'climb.csv', index_col=0)
    power_df = pd.read_csv(performance_path + '\\' + 'power.csv',)
    range40_df = pd.read_csv(performance_path + '\\' + 'range40.csv', index_col=0)
    range50_df = pd.read_csv(performance_path + '\\' + 'range50.csv', index_col=0)
    endurance40_df = pd.read_csv(performance_path + '\\' + 'endurance40.csv', index_col=0)
    endurance50_df = pd.read_csv(performance_path + '\\' + 'endurance50.csv', index_col=0)
    landing_df = pd.read_csv(performance_path + '\\' + 'landing.csv', index_col=1)

    # Generate valid performance data.
    data.compute_valid_performance_data(input_data, power_df)

    # Compute wind intensity and direction for takeoff, cruise and landing.
    wind.run_wind_analysis(input_data)

    # Compute takeoff performance.
    to_roll, to_50_roll, roc = takeoff.compute_takeoff_performance(input_data, takeoff_df, roc_df)

    # Compute cruise performance.
    if input_data['fuel_capacity'] == 40:
        range_df = range40_df
        endurance_df = endurance40_df
    else:
        range_df = range50_df
        endurance_df = endurance50_df
    max_endurance, max_range, ktas, fuel_flow = cruise.compute_cruise_performance(input_data, power_df, range_df, endurance_df)

    # Compute fuel required.
    fuel_required, fuel_reserve = fuel.compute_fuel_required(input_data, climb_df, ktas, fuel_flow)

    # Compute landing performance.
    land_roll, land_50_roll = landing.compute_landing_performance(input_data, landing_df)

    # Store results.
    keys = ['to_roll', 'to_50_roll', 'to_roc', 'max_endurance', 'max_range', 'fuel_required', 'fuel_reserve', 'land_roll', 'land_50_roll']
    values = [to_roll, to_50_roll, roc, max_endurance, max_range, fuel_required, fuel_reserve, land_roll, land_50_roll]
    results = {}
    for (key, value) in zip(keys, values):
        results[key] = value
    return results


if __name__ == '__main__':
    # TODO: add testing functionality.
    print("Run directly")
    