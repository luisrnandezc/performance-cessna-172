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


def correct_distance_for_wind(ground_roll, fifty_ft_roll, wind_speed, wind_direction):
    """Returns the landing distances corrected for wind.

    This function corrects the minimum landing distances considering
    the direction and intensity of the wind.

    Args:
        ground_roll (int): minimum required landing distance.
        fifty_ft_roll (int): distance required to clear a 50 ft obstacle.
        wind_speed (int): landing wind speed in knots.
        wind_direction (str): landing wind direction.

    Returns:
        ground_roll (int): corrected minimum required landing distance.
        fifty_ft_roll (int): corrected distance required to clear a 50 ft obstacle.
    """
    if wind_speed != 0:
        if wind_direction == 'H':
            corr = -1*round((wind_speed*0.1)/9, 2)
        else:
            corr = round((wind_speed*0.1)/2, 2)
        ground_roll = math.ceil(ground_roll + ground_roll*corr)
        fifty_ft_roll = math.ceil(fifty_ft_roll + fifty_ft_roll*corr)
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
    if condition == 'g':
        corr = round(ground_roll*0.45, 2)
        ground_roll = math.ceil(ground_roll + corr)
        fifty_ft_roll = math.ceil(fifty_ft_roll + corr)
    return ground_roll, fifty_ft_roll


def compute_landing_performance(input_data, landing_df):
    press_alt = input_data['land_press_alt']
    temp = input_data['land_temp']
    # Read the landing distance from the table.
    ground_roll, fifty_ft_roll = compute_landing_ground_roll(press_alt, temp, landing_df)
    # Correct landing distance for wind.
    wind_speed = input_data['land_wind_speed']
    wind_direction = input_data['land_wind_direction']
    ground_roll, fifty_ft_roll = correct_distance_for_wind(ground_roll, fifty_ft_roll, wind_speed, wind_direction)
    # Correct landing distance for runway condition.
    condition = input_data['land_condition']
    ground_roll, fifty_ft_roll = correct_distance_for_runway_condition(ground_roll, fifty_ft_roll, condition)
    return int(ground_roll), int(fifty_ft_roll)
