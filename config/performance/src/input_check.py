"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023

NAME:
    input.py

DESCRIPTION:
    This module checks that the input data is valid and within limits.

    The purpose of this module is to ensure that 1) all the user input data
    is physically valid, e.g., a distance can't be negative, and 2) the data
    is within the expected limits, e.g., the cruise altitude can't be higher
    than 14.200 ft. For example, if the user enters a negative value of
    takeoff runway length, the program stops with an appropriate error
    message indicating that a runway length can't be negative.

"""


import sys

# Error messages.
msg_error_invalid_value = "ERROR: invalid value."
msg_error_negative_value = "ERROR: the value can't be negative."
msg_error_big_value = "ERROR: the value is too big."
msg_error_small_value = "ERROR: the value is to small."


def check_if_value_is_numeric(value):
    """Returns True if the argument is a number, False otherwise."""
    try:
        int(value)
    except ValueError:
        return False
    return True


def check_if_value_is_negative(value):
    """Returns True if the argument is a positive number, False otherwise."""
    if int(value) < 0:
        return True
    return False


def check_take_off_weight(to_weight):
    """
    Returns None if the argument is a valid aircraft weight,
    otherwise the programs stops with a custom error message.
    """
    if check_if_value_is_numeric(to_weight) is False:
        sys.exit('Takeoff weight | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(to_weight) is True:
        sys.exit('Takeoff weight | ' + msg_error_negative_value)
    elif int(to_weight) < 1397 or int(to_weight) > 2300:
        sys.exit('Takeoff weight | ERROR: The weight must be between 1397 and 2300 pounds.')
    else:
        return None


def check_fuel_capacity(fuel_capacity):
    """
    Returns None if the argument is a valid fuel capacity,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(fuel_capacity) is False:
        sys.exit('Fuel capacity | ' + msg_error_invalid_value)
    elif int(fuel_capacity) != 40 and int(fuel_capacity) != 50:
        sys.exit('Fuel capacity | ' + msg_error_invalid_value)
    else:
        return None


def check_runway_number(rwy_number):
    """
    Returns None if the argument is a valid runway number,
    otherwise the program stops with a pertinent error message.
    """
    if rwy_number < 1 or rwy_number > 36:
        sys.exit('Runway number | ' + msg_error_invalid_value)
    return None


def check_runway_length(rwy_length):
    """
    Returns None if the argument is a valid runway length,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(rwy_length) is False:
        sys.exit('The runway length | ' + msg_error_invalid_value)
    elif int(rwy_length) <= 0:
        sys.exit('The runway length | ' + msg_error_invalid_value)
    else:
        return None


def check_runway_condition(rwy_condition):
    """
    Returns None if the argument is a valid runway condition,
    otherwise the program stops with a pertinent error message.
    """
    valid_conditions = ['PD', 'GD']
    if rwy_condition not in valid_conditions:
        sys.exit('Runway condition | ' + msg_error_invalid_value)
    else:
        return None


def check_pressure_altitude(press_altitude):
    """
    Returns None if the argument is a valid pressure altitude,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(press_altitude) is False:
        sys.exit('Pressure altitude | ' + msg_error_invalid_value)
    elif int(press_altitude) < 0 or int(press_altitude) > 14200:
        sys.exit('Pressure altitude | ERROR: The pressure altitude must be between 0 and 14200 feets.')
    else:
        return None


def check_temperature(temperature):
    """
    Returns None if the argument is a valid temperature,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(temperature) is False:
        sys.exit('Temperature | ' + msg_error_invalid_value)
    elif int(temperature) < -20 or int(temperature) > 40:
        sys.exit('Temperature | ERROR: The temperature must be between -20 and 40 degrees Celsius.')
    else:
        return None


def check_wind_speed(wind_speed):
    """
    Returns None if the argument is a valid wind speed,
    otherwise the program stops with a pertinent error message.
    """
    if int(wind_speed) == 0:
        return None
    elif check_if_value_is_numeric(wind_speed) is False:
        sys.exit('Wind speed | ' + msg_error_invalid_value)
    elif wind_speed < 0 or wind_speed > 50:
        sys.exit('Wind speed | ERROR: The wind speed must be between 0 and 50 knots.')
    else:
        return None


def check_wind_direction(wind_direction):
    """
    Returns None if the argument is a valid wind direction,
    otherwise the program stops with a pertinent error message.
    """
    if wind_direction < 1 or wind_direction > 360 or wind_direction % 5 != 0:
        sys.exit('Wind direction | ' + msg_error_invalid_value)
    return None


def check_travel_distance(travel_distance):
    """
    Returns None if the argument is a valid distance,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(travel_distance) is False:
        sys.exit('Travel distance | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(travel_distance) is True:
        sys.exit('Travel distance | ' + msg_error_negative_value)
    elif travel_distance < 0 or travel_distance > 750:
        sys.exit('Travel distance | ERROR: The distance must be between 0 and 750 nautical miles.')
    else:
        return None


def check_cr_heading(cr_heading):
    """
    Returns None if the argument is a valid cruise heading,
    otherwise the program stops with a pertinent error message.
    """
    if cr_heading < 1 or cr_heading > 36:
        sys.exit('Cruise heading | ' + msg_error_invalid_value)
    return None


def check_cruise_rpm(cr_rpm):
    """
    Returns None if the argument is a valid cruise rpm,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(cr_rpm) is False:
        sys.exit('Cruise rpm | ' + msg_error_invalid_value)
    elif cr_rpm < 2100 or cr_rpm > 2650:
        sys.exit('Cruise rpm | ERROR: The rpm must be between 2100 and 2650.')
    else:
        return None


def check_input_data(input_data):
    """
    Checks the validity of the data entered by the user.

        > If the data is valid the function returns a
        dictionary with the validated data.
        > Else, the program stops with an error message
        indicating the source of the error.

    Args:
        input_data: dict containing the raw user input data.

    Returns:
        input_data: dictionary of validated input data.
    """

    # Check general data.
    check_take_off_weight(input_data['to_weight'])
    check_fuel_capacity(input_data['fuel_capacity'])
    # Check takeoff data.
    check_runway_number(input_data['to_rwy'])
    check_runway_length(input_data['to_length'])
    check_runway_condition(input_data['to_condition'])
    check_pressure_altitude(input_data['to_press_alt'])
    check_temperature(input_data['to_temp'])
    check_wind_speed(input_data['to_wind_speed'])
    check_wind_direction(input_data['to_wind_direction'])
    # Check cruise data.
    check_travel_distance(input_data['travel_dist'])
    check_cr_heading(input_data['cr_heading'])
    check_pressure_altitude(input_data['cr_press_alt'])
    check_temperature(input_data['cr_temp'])
    check_wind_speed(input_data['cr_wind_speed'])
    check_wind_direction(input_data['cr_wind_direction'])
    check_cruise_rpm(input_data['cr_power'])
    # Check landing data.
    check_runway_number(input_data['land_rwy'])
    check_runway_length(input_data['land_length'])
    check_runway_condition(input_data['land_condition'])
    check_pressure_altitude(input_data['land_press_alt'])
    check_temperature(input_data['land_temp'])
    check_wind_speed(input_data['land_wind_speed'])
    check_wind_direction(input_data['land_wind_direction'])

    return input_data
