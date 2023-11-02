"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023
"""


import sys

# Error messages.
msg_error_invalid_value = 'ERROR: el valor introducido es inválido.'
msg_error_negative_value = 'ERROR: el valor introducido no puede ser negativo.'
msg_error_excessive_value = 'ERROR: el valor introducido es muy alto.'
msg_error_low_value = 'ERROR: el valor introducido es muy bajo.'


# Main functions.
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


def check_takeoff_runway_length(to_rwy_length):
    """
    Returns None if the argument is a valid runway length,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(to_rwy_length) is False:
        sys.exit('Takeoff runway length | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(to_rwy_length) is True:
        sys.exit('Takeoff runway length | ' + msg_error_negative_value)
    elif int(to_rwy_length) == 0:
        sys.exit('Takeoff runway length | ' + msg_error_invalid_value)
    else:
        return None


def check_takeoff_runway_condition(to_rwy_condition):
    """
    Returns None if the argument is a valid runway condition,
    otherwise the program stops with a pertinent error message.
    """
    valid_conditions = ['PD', 'GD']
    if to_rwy_condition not in valid_conditions:
        sys.exit('Takeoff runway condition | ' + msg_error_invalid_value)
    else:
        return None


def check_takeoff_pressure_altitude(to_press_altitude):
    """
    Returns None if the argument is a valid pressure altitude,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(to_press_altitude) is False:
        sys.exit('Takeoff pressure altitude | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(to_press_altitude) is True:
        sys.exit('Takeoff pressure altitude | ' + msg_error_negative_value)
    elif int(to_press_altitude) > 14200:
        sys.exit('Takeoff pressure altitude | Error: el valor introducido es mayor al Techo de Servicio.')
    else:
        return None


def check_takeoff_temperature(to_temperature):
    """
    Returns None if the argument is a valid takeoff temperature,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(to_temperature) is False:
        sys.exit('Takeoff temperature | ' + msg_error_invalid_value)
    elif int(to_temperature) > 40:
        sys.exit('Takeoff temperature | ' + msg_error_excessive_value)
    elif int(to_temperature) < -20:
        sys.exit('Takeoff temperature | ' + msg_error_low_value)
    else:
        return None


def check_takeoff_wind(to_wind):
    """
    Returns None if the argument is a valid takeoff wind value,
    otherwise the program stops with a pertinent error message.
    """
    if to_wind == '0':
        return None
    if len(to_wind) != 3:
        sys.exit('Takeoff wind | ' + msg_error_invalid_value)
    knots = to_wind[0] + to_wind[1]
    direction = to_wind[-1]
    if check_if_value_is_numeric(knots) is False:
        sys.exit('Takeoff wind | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(knots) is True:
        sys.exit('Takeoff wind | ' + msg_error_negative_value)
    elif direction != 'H' and direction != 'T':
        sys.exit('Takeoff wind | ' + msg_error_invalid_value)
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


def check_cruise_pressure_altitude(cr_press_altitude):
    """
    Returns None if the argument is a valid cruise pressure altitude,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(cr_press_altitude) is False:
        sys.exit('Cruise pressure altitude | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(cr_press_altitude) is True:
        sys.exit('Cruise pressure altitude | ' + msg_error_negative_value)
    elif int(cr_press_altitude) > 14200:
        sys.exit('Cruise pressure altitude | ERROR: el valor introducido es mayor al Techo de Servicio.')
    else:
        return None


def check_cruise_temperature(cr_temperature):
    """
    Returns None if the argument is a valid cruise temperature,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(cr_temperature) is False:
        sys.exit('Cruise temperature | ' + msg_error_invalid_value)
    elif int(cr_temperature) > 40:
        sys.exit('Cruise temperature | ' + msg_error_excessive_value)
    elif int(cr_temperature) < -30:
        sys.exit('Cruise temperature | ' + msg_error_low_value)
    else:
        return None


def check_cruise_wind(cr_wind):
    """
    Returns None if the argument is a valid cruise wind value,
    otherwise the program stops with a pertinent error message.
    """
    if cr_wind == '0':
        return None
    if len(cr_wind) != 3:
        sys.exit('Cruise wind | ' + msg_error_invalid_value)
    knots = cr_wind[0] + cr_wind[1]
    direction = cr_wind[-1]
    if check_if_value_is_numeric(knots) is False:
        sys.exit('Cruise wind | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(knots) is True:
        sys.exit('Cruise wind | ' + msg_error_negative_value)
    elif direction != 'H' and direction != 'T':
        sys.exit('Cruise wind | ' + msg_error_invalid_value)
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


def check_landing_runway_length(land_rwy_length):
    """
    Returns None if the argument is a valid runway length,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(land_rwy_length) is False:
        sys.exit('Landing runway length | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(land_rwy_length) is True:
        sys.exit('Landing runway length | ' + msg_error_negative_value)
    elif int(land_rwy_length) == 0:
        sys.exit('Landing runway length | ' + msg_error_invalid_value)
    else:
        return None


def check_landing_runway_condition(land_rwy_condition):
    """
    Returns None if the argument is a valid runway condition,
    otherwise the program stops with a pertinent error message.
    """
    valid_conditions = ['PD', 'GD']
    if land_rwy_condition not in valid_conditions:
        sys.exit('Landing runway condition | ' + msg_error_invalid_value)
    else:
        return None


def check_landing_pressure_altitude(land_press_altitude):
    """
    Returns None if the argument is a valid pressure altitude,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(land_press_altitude) is False:
        sys.exit('Landing pressure altitude | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(land_press_altitude) is True:
        sys.exit('Landing pressure altitude | ' + msg_error_negative_value)
    elif int(land_press_altitude) > 14200:
        sys.exit('Landing pressure altitude | ERROR: el valor introducido es mayor al Techo de Servicio.')
    else:
        return None


def check_landing_temperature(land_temperature):
    """
    Returns None if the argument is a valid landing temperature,
    otherwise the program stops with a pertinent error message.
    """
    if check_if_value_is_numeric(land_temperature) is False:
        sys.exit('Landing temperature | ' + msg_error_invalid_value)
    elif int(land_temperature) > 40:
        sys.exit('Landing temperature | ' + msg_error_excessive_value)
    elif int(land_temperature) < -20:
        sys.exit('Landing temperature | ' + msg_error_low_value)
    else:
        return None


def check_landing_wind(land_wind):
    """
    Returns None if the argument is a valid wind value,
    otherwise the program stops with a pertinent error message.
    """
    if land_wind == '0':
        return None
    if len(land_wind) != 3:
        sys.exit('Landing wind | ' + msg_error_invalid_value)
    knots = land_wind[0] + land_wind[1]
    direction = land_wind[-1]
    if check_if_value_is_numeric(knots) is False:
        sys.exit('Landing wind | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(knots) is True:
        sys.exit('Landing wind | ' + msg_error_negative_value)
    elif direction != 'H' and direction != 'T':
        sys.exit('Landing wind | ' + msg_error_invalid_value)
    else:
        return None


def check_input_data(file):
    """
    This function checks the validity of the data
    entered by the user.

        > If the data is valid the function returns a
        dictionary with the validated data.

        > Else, the program stops with an error message
        indicating the source of the error.

    :argument:
        file: file containing the raw user input data.
    :returns:
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
    check_takeoff_runway_length(input_data['TOL'])
    check_takeoff_runway_condition(input_data['TOC'])
    check_takeoff_pressure_altitude(input_data['TOPA'])
    check_takeoff_temperature(input_data['TOT'])
    check_takeoff_wind(input_data['TOW'])
    # Check cruise data.
    check_travel_distance(input_data['TD'])
    check_cruise_pressure_altitude(input_data['CRPA'])
    check_cruise_temperature(input_data['CRT'])
    check_cruise_wind(input_data['CRW'])
    check_cruise_rpm(input_data['RPM'])
    # Check landing data.
    check_landing_runway_length(input_data['LDL'])
    check_landing_runway_condition(input_data['LDC'])
    check_landing_pressure_altitude(input_data['LDPA'])
    check_landing_temperature(input_data['LDT'])
    check_landing_wind(input_data['LDW'])

    return input_data
