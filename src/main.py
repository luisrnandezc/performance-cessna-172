"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023
"""

import input_check
import data
import takeoff
import cruise
import fuel
import landing
import output
import pandas as pd
import openpyxl


if __name__ == '__main__':
    # Read input and output path.
    path = input("Ubicación del archivo de datos: ")

    # Read input data.
    input_file = open(path + '\\' + 'input.txt', 'r')

    # Check input data.
    input_data = input_check.check_input_data(input_file)

    # Store performance data.
    performance_path = r'C:\Users\luish\Desktop\Projects\performance_cessna_172\data'
    takeoff_df = pd.read_csv(performance_path + '\\' + 'takeoff.csv')
    roc_df = pd.read_csv(performance_path + '\\' + 'roc.csv', index_col=0)
    climb_df = pd.read_csv(performance_path + '\\' + 'climb.csv', index_col=0)
    power_df = pd.read_csv(performance_path + '\\' + 'power.csv',)
    range40_df = pd.read_csv(performance_path + '\\' + 'range40.csv', index_col=0)
    range50_df = pd.read_csv(performance_path + '\\' + 'range50.csv', index_col=0)
    endurance40_df = pd.read_csv(performance_path + '\\' + 'endurance40.csv', index_col=0)
    endurance50_df = pd.read_csv(performance_path + '\\' + 'endurance50.csv', index_col=0)
    landing_df = pd.read_csv(performance_path + '\\' + 'landing.csv', index_col=1)
    atm_df = pd.read_csv(performance_path + '\\' + 'atm.csv', index_col=1)

    # Generate valid performance data.
    valid_data = data.compute_valid_performance_data(input_data, power_df)

    # Compute takeoff performance.
    takeoff_ground_roll, takeoff_fifty_ft_roll, roc = takeoff.compute_takeoff_performance(input_data, takeoff_df, roc_df)

    # Compute cruise performance.
    if input_data['FC'] == 40:
        range_df = range40_df
        endurance_df = endurance40_df
    else:
        range_df = range50_df
        endurance_df = endurance50_df
    max_endurance, max_range, velocity, fuel_flow = cruise.compute_cruise_performance(input_data, power_df, range_df, endurance_df)

    # Compute fuel required.
    fuel_required, fuel_reserve = fuel.compute_fuel_required(input_data, climb_df, velocity, fuel_flow)

    # Compute landing performance.
    land_ground_roll, land_fifty_roll = landing.compute_landing_performance(input_data, landing_df)

    # Generate performance file.
    results = [takeoff_ground_roll, takeoff_fifty_ft_roll,
               max_endurance, max_range, fuel_required, fuel_reserve,
               land_ground_roll, land_fifty_roll]
    output_data = output.write_output_file(results, path)
