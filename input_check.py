"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc

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
msg_error_invalid_value = 'ERROR: el valor introducido es inválido.'
msg_error_negative_value = 'ERROR: el valor introducido no puede ser negativo.'
msg_error_excessive_value = 'ERROR: el valor introducido es muy alto.'
msg_error_low_value = 'ERROR: el valor introducido es muy bajo.'


def check_if_value_is_numeric(value):
    """Returns True if the argument is a number, False otherwise."""
    try:
        value = int(value)
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
    elif int(to_weight) > 2300:
        sys.exit('Peso de despegue | ERROR: el peso introducido es mayor al peso máximo.')
    elif int(to_weight) < 1397:
        sys.exit('Peso de despegue | ERROR: el peso introducido es menor al peso vacío estándar.')
    else:
        return None


def check_fuel_capacity(fuel_capacity):
    """
    Returns None if the argument is a valid fuel capacity,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(fuel_capacity) is False:
        sys.exit('Fuel Capacity | ' + msg_error_invalid_value)
    elif int(fuel_capacity) != 40 and int(fuel_capacity) != 50:
        sys.exit('Fuel Capacity | ' + msg_error_invalid_value)
    else:
        return None


def check_runway_length(rwy_length):
    """
    Returns None if the argument is a valid runway length,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(rwy_length) is False:
        sys.exit('The runway length | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(rwy_length) is True:
        sys.exit('The runway length | ' + msg_error_negative_value)
    elif int(rwy_length) == 0:
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
    elif check_if_value_is_negative(press_altitude) is True:
        sys.exit('Pressure altitude | ' + msg_error_negative_value)
    elif int(press_altitude) > 14200:
        sys.exit('Pressure altitude | Error: el valor introducido es mayor al Techo de Servicio.')
    else:
        return None


def check_temperature(temperature):
    """
    Returns None if the argument is a valid temperature,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(temperature) is False:
        sys.exit('Temperature | ' + msg_error_invalid_value)
    elif int(temperature) > 40:
        sys.exit('Temperature | ' + msg_error_excessive_value)
    elif int(temperature) < -20:
        sys.exit('Temperature | ' + msg_error_low_value)
    else:
        return None


def check_wind(wind):
    """
    Returns None if the argument is a valid wind value,
    otherwise the program stops with a pertinent error message.
    """
    if wind == '0':
        return None
    if len(wind) != 3:
        sys.exit('Takeoff wind | ' + msg_error_invalid_value)
    knots = wind[0:2]
    direction = wind[-1]
    if check_if_value_is_numeric(knots) is False:
        sys.exit('Wind | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(knots) is True:
        sys.exit('Wind | ' + msg_error_negative_value)
    elif direction != 'H' and direction != 'T':
        sys.exit('Wind | ' + msg_error_invalid_value)
    else:
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
    else:
        return None


def check_cruise_rpm(cr_rpm):
    """
    Returns None if the argument is a valid cruise rpm,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(cr_rpm) is False:
        sys.exit('Cruise rpm | ' + msg_error_invalid_value)
    cr_rpm = int(cr_rpm)
    if cr_rpm < 2100:
        sys.exit('Cruise rpm | ' + msg_error_low_value + ' El valor mínimo es 2100 rpm.')
    elif cr_rpm > 2650:
        sys.exit('Cruise rpm | ' + msg_error_excessive_value + ' El valor máximo es 2650 rpm.')
    return None


def check_input_data(file):
    """
    Checks the validity of the data entered by the user.

        > If the data is valid the function returns a
        dictionary with the validated data.
        > Else, the program stops with an error message
        indicating the source of the error.

    Args:
        file: file containing the raw user input data.

    Returns:
        input_data: dictionary of validated input data.
    """

    # Read the data.
    lines = file.readlines()
    values = []
    for line in lines:
        line = line[:-1]
        values.append(line.upper())
    # Store data into a dictionary.
    keys = ['TOWG', 'FC', 'TOL', 'TOC', 'TOPA', 'TOT', 'TOW',
            'TD', 'CRPA', 'CRT', 'CRW', 'RPM',
            'LDL', 'LDC', 'LDPA', 'LDT', 'LDW']
    input_data = {key: value for (key, value) in zip(keys, values)}

    # Check general data.
    check_take_off_weight(input_data['TOWG'])
    check_fuel_capacity(input_data['FC'])
    # Check takeoff data.
    check_runway_length(input_data['TOL'])
    check_runway_condition(input_data['TOC'])
    check_pressure_altitude(input_data['TOPA'])
    check_temperature(input_data['TOT'])
    check_wind(input_data['TOW'])
    # Check cruise data.
    check_travel_distance(input_data['TD'])
    check_pressure_altitude(input_data['CRPA'])
    check_temperature(input_data['CRT'])
    check_wind(input_data['CRW'])
    check_cruise_rpm(input_data['RPM'])
    # Check landing data.
    check_runway_length(input_data['LDL'])
    check_runway_condition(input_data['LDC'])
    check_pressure_altitude(input_data['LDPA'])
    check_temperature(input_data['LDT'])
    check_wind(input_data['LDW'])

    return input_data
