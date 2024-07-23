"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023

NAME:
    landing.py

DESCRIPTION:
    The objective of this module is to compute the landing
    performance. Two values are obtained:

    > ground_roll [ft]
        Minimum required landing distance.
    > fifty_ft_roll [ft]
        Distance required to clear an obstacle located 50 ft above the runway
        threshold. It is always bigger than the ground_roll distance.
"""


import math


def compute_landing_ground_roll(press_alt, temp, landing_df):
    """Returns the required landing distances.

    This function computes the minimum landing distance considering the
    airport pressure altitude, airport temperature, and performance data.

    Args:
        press_alt (int): landing pressure altitude.
        temp (int): landing temperature.
        landing_df: landing performance dataframe.

    Returns:
        ground_roll (int): minimum required landing distance.
        fifty_ft_roll (int): distance required to clear a 50 ft obstacle.
    """
    takeoff_df = landing_df[(landing_df['press_alt'] == press_alt)]
    ground_roll = takeoff_df.iloc[0][str(temp) + '_celsius_gr_roll']
    fifty_ft_roll = takeoff_df.iloc[0][str(temp) + '_celsius_50_ft']
    return ground_roll, fifty_ft_roll


def correct_distance_for_wind(ground_roll, fifty_ft_roll, wind):
    """Returns the landing distances corrected for wind.

    This function corrects the minimum landing distances considering
    the direction and intensity of the wind.

    Args:
        ground_roll (int): minimum required landing distance.
        fifty_ft_roll (int): distance required to clear a 50 ft obstacle.
        wind (str): landing wind component.

    Returns:
        ground_roll (int): corrected minimum required landing distance.
        fifty_ft_roll (int): corrected distance required to clear a 50 ft obstacle.
    """
    if wind != 0:
        knots = wind[0:2]
        direction = wind[-1]
        if direction == 'H':
            correction = round((int(knots)*0.1)/9, 2)
            corrected_ground_roll = math.ceil(ground_roll - ground_roll*correction)
            corrected_fifty_ft_roll = math.ceil(fifty_ft_roll - fifty_ft_roll*correction)
            return corrected_ground_roll, corrected_fifty_ft_roll
        else:
            correction = round((int(knots)*0.1)/2, 2)
            corrected_ground_roll = math.ceil(ground_roll + ground_roll*correction)
            corrected_fifty_ft_roll = math.ceil(fifty_ft_roll + fifty_ft_roll*correction)
            return corrected_ground_roll, corrected_fifty_ft_roll
    else:
        return ground_roll, fifty_ft_roll


def correct_distance_for_runway_condition(ground_roll, fifty_ft_roll, condition):
    """Returns the landing distances corrected for runway condition.

    Args:
        ground_roll (int): minimum required landing distance.
        fifty_ft_roll (int): distance required to clear a 50 ft obstacle.
        condition (str): landing runway condition.

    Returns:
        ground_roll (int): corrected minimum required landing distance.
        fifty_ft_roll (int): corrected distance required to clear a 50 ft obstacle.
    """
    if condition == 'GD':
        correction = round(ground_roll*0.45, 2)
        corrected_ground_roll = math.ceil(ground_roll + correction)
        corrected_fifty_ft_roll = math.ceil(fifty_ft_roll + correction)
        return corrected_ground_roll, corrected_fifty_ft_roll
    else:
        return ground_roll, fifty_ft_roll


def compute_landing_performance(input_data, landing_df):
    press_alt = input_data['LDPA']
    temp = input_data['LDT']
    # Read the landing distance from the table.
    ground_roll, fifty_ft_roll = compute_landing_ground_roll(press_alt, temp, landing_df)
    # Correct landing distance for wind.
    wind = input_data['LDW']
    ground_roll, fifty_ft_roll = correct_distance_for_wind(ground_roll, fifty_ft_roll, wind)
    # Correct landing distance for runway condition.
    condition = input_data['LDC']
    ground_roll, fifty_ft_roll = correct_distance_for_runway_condition(ground_roll, fifty_ft_roll, condition)
    return ground_roll, fifty_ft_roll
