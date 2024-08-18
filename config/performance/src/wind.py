"""
Cessna 172N Performance Calculator
Author: Luis Hernandez
GitHub: luisrnandezc

NAME:
    wind.py

DESCRIPTION:
    This module computes the wind component in takeoff, cruise and landing.

    The purpose of this module is to compute the wind speed and direction
    for takeoff, cruise and landing. The objective is to reduce the user
    workload and enhance the final results accuracy.

"""


import math


def compute_wind_component(heading, wind_speed, wind_direction):
    """Returns the wind component parallel to the aircraft."""
    angle = abs(heading - wind_direction)
    if angle == 90 or angle == 270:
        return 0, None
    aligned_speed = abs(round(wind_speed*math.cos(math.radians(angle)), 1))
    if 90 < angle < 270:
        aligned_direction = 'T'
    else:
        aligned_direction = 'H'
    return aligned_speed, aligned_direction


def run_wind_analysis(input_data):
    """
    Updates the input_data dictionary with wind components for takeoff,
    cruise and landing.
    """
    # Compute wind components for takeoff, cruise and landing.
    to_rwy = input_data['to_rwy']
    to_wind_speed = input_data['to_wind_speed']
    to_wind_direction = input_data['to_wind_direction']
    to_wind_component = compute_wind_component(to_rwy, to_wind_speed, to_wind_direction)
    cr_heading = input_data['cr_heading']
    cr_wind_speed = input_data['cr_wind_speed']
    cr_wind_direction = input_data['cr_wind_direction']
    cr_wind_component = compute_wind_component(cr_heading, cr_wind_speed, cr_wind_direction)
    land_rwy = input_data['land_rwy']
    land_wind_speed = input_data['land_wind_speed']
    land_wind_direction = input_data['land_wind_direction']
    land_wind_component = compute_wind_component(land_rwy, land_wind_speed, land_wind_direction)
    # Update input data with computed wind components.
    input_data['to_wind_speed'] = to_wind_component[0]
    input_data['to_wind_direction'] = to_wind_component[1]
    input_data['cr_wind_speed'] = cr_wind_component[0]
    input_data['cr_wind_direction'] = cr_wind_component[1]
    input_data['land_wind_speed'] = land_wind_component[0]
    input_data['land_wind_direction'] = land_wind_component[1]
    return None
