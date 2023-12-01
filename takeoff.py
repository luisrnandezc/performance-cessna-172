"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023

NAME:
    takeoff.py

DESCRIPTION:
    The objective of this module is to compute the takeoff
    performance. Three values are obtained:

    > ground_roll [ft]
        Minimum required takeoff distance
    > fifty_ft_roll [ft]
        Distance required to clear an obstacle located 50 ft above the runway.
        It is always bigger than the ground_roll distance.
    > roc [ft/s]
        Maximum Rate of Climb expected immediately after takeoff.
"""

import math


def compute_takeoff_ground_roll(weight, press_alt, temp, takeoff_df):
    """Returns the required takeoff distances.

    This function computes the minimum takeoff distance considering the
    aircraft weight, airport temperature, airport pressure altitude
    and performance data.

    Args:
        weight (int): aircraft takeoff weight.
        press_alt (int): takeoff pressure altitude.
        temp (int): takeoff temperature.
        takeoff_df: takeoff performance dataframe.

    Returns:
        ground_roll (int): minimum required takeoff distance.
        fifty_ft_roll (int): distance required to clear a 50 ft obstacle.
    """
    takeoff_df = takeoff_df[(takeoff_df['weight'] == weight) & (takeoff_df['press_alt'] == press_alt)]
    ground_roll = takeoff_df.iloc[0][str(temp) + '_celsius_gr_roll']
    fifty_ft_roll = takeoff_df.iloc[0][str(temp) + '_celsius_50_ft']
    return ground_roll, fifty_ft_roll


def correct_distance_for_wind(ground_roll, fifty_ft_roll, wind):
    """Returns the takeoff distances corrected for wind.

    This function corrects the minimum takeoff distances considering
    the direction and intensity of the wind.

    Args:
        ground_roll (int): minimum required takeoff distance.
        fifty_ft_roll (int): distance required to clear a 50 ft obstacle.
        wind (str): takeoff wind component.

    Returns:
        ground_roll (int): corrected minimum required takeoff distance.
        fifty_ft_roll (int): corrected distance required to clear a 50 ft obstacle.
    """
    if wind != 0:
        knots = wind[0:2]
        direction = wind[-1]
        if direction == 'H':
            corr = -1*round((int(knots)*0.1)/9, 2)
        else:
            corr = round((int(knots)*0.1)/2, 2)
        ground_roll = math.ceil(ground_roll + ground_roll*corr)
        fifty_ft_roll = math.ceil(fifty_ft_roll + fifty_ft_roll*corr)
    return ground_roll, fifty_ft_roll


def correct_distance_for_runway_condition(ground_roll, fifty_ft_roll, condition):
    """Returns the takeoff distances corrected for runway condition.

    Args:
        ground_roll (int): minimum required takeoff distance.
        fifty_ft_roll (int): distance required to clear a 50 ft obstacle.
        condition (str): takeoff runway condition.

    Returns:
        ground_roll (int): corrected minimum required takeoff distance.
        fifty_ft_roll (int): corrected distance required to clear a 50 ft obstacle.
    """
    if condition == 'GD':
        corr = round(ground_roll*0.15, 2)
        ground_roll = math.ceil(ground_roll + corr)
        fifty_ft_roll = math.ceil(fifty_ft_roll + corr)
    return ground_roll, fifty_ft_roll


def compute_takeoff_roc(press_alt, roc_temp, roc_df):
    """Returns the takeoff Rate of Climb (ROC).

    Args:
        press_alt (int): takeoff pressure altitude.
        roc_temp (int): takeoff temperature.
        roc_df: rate of climb dataframe.

    Returns:
        roc (int): rate of climb in ft/min.
    """
    if roc_temp < 0:
        roc = roc_df.loc[press_alt]['roc_m' + str(roc_temp)]
    elif roc_temp > 0:
        roc = roc_df.loc[press_alt]['roc_p' + str(roc_temp)]
    else:
        roc = roc_df.loc[press_alt]['roc_' + str(roc_temp)]
    return roc


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
