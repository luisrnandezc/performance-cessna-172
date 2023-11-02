"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023
"""


import math


def compute_takeoff_ground_roll(weight, press_alt, temp, takeoff_df):
    takeoff_df = takeoff_df[(takeoff_df['weight'] == weight) & (takeoff_df['press_alt'] == press_alt)]
    ground_roll = takeoff_df.iloc[0][str(temp) + '_celsius_gr_roll']
    fifty_ft_roll = takeoff_df.iloc[0][str(temp) + '_celsius_50_ft']
    return ground_roll, fifty_ft_roll


def correct_distance_for_wind(ground_roll, fifty_ft_roll, wind):
    if wind != 0:
        knots = wind[0:2]
        direction = wind[-1]
        if direction == 'H':
            correction = round((int(knots)*0.1)/9, 2)
            corrected_ground_roll = math.ceil(ground_roll - ground_roll*correction)
            corrected_fifty_ft_roll = math.ceil(fifty_ft_roll - fifty_ft_roll*correction)
            return corrected_ground_roll, corrected_fifty_ft_roll
        else:
            correction = round((int(knots)*0.1)/2, 2) + 1
            corrected_ground_roll = math.ceil(ground_roll*correction)
            corrected_fifty_ft_roll = math.ceil(fifty_ft_roll*correction)
            return corrected_ground_roll, corrected_fifty_ft_roll
    else:
        return ground_roll, fifty_ft_roll


def correct_distance_for_runway_condition(ground_roll, fifty_ft_roll, condition):
    if condition == 'GD':
        correction = round(ground_roll*0.15, 2)
        corrected_ground_roll = math.ceil(ground_roll + correction)
        corrected_fifty_ft_roll = math.ceil(fifty_ft_roll + correction)
        return corrected_ground_roll, corrected_fifty_ft_roll
    else:
        return ground_roll, fifty_ft_roll


def compute_takeoff_roc(press_alt, roc_temp, roc_df):
    if roc_temp < 0:
        return roc_df.loc[press_alt]['roc_m' + str(roc_temp)]
    elif roc_temp > 0:
        return roc_df.loc[press_alt]['roc_p' + str(roc_temp)]
    else:
        return roc_df.loc[press_alt]['roc_' + str(roc_temp)]


def compute_takeoff_performance(input_data, takeoff_df, roc_df):
    weight = input_data['TOWG']
    press_alt = input_data['TOPA']
    temp = input_data['TOT']
    # Read the takeoff distance from the table.
    ground_roll, fifty_ft_roll = compute_takeoff_ground_roll(weight, press_alt, temp, takeoff_df)
    # Correct takeoff distance for wind.
    wind = input_data['TOW']
    ground_roll, fifty_ft_roll = correct_distance_for_wind(ground_roll, fifty_ft_roll, wind)
    # Correct takeoff distance for runway condition.
    condition = input_data['TOC']
    ground_roll, fifty_ft_roll = correct_distance_for_runway_condition(ground_roll, fifty_ft_roll, condition)
    # Compute takeoff rate of climb.
    roc_press_alt = input_data['ROCPA']
    roc_temp = input_data['ROCT']
    roc = compute_takeoff_roc(roc_press_alt, roc_temp, roc_df)
    return ground_roll, fifty_ft_roll, roc
