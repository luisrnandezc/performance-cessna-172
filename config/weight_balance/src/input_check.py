"""
Cessna 172N Weight and Balance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023

NAME:
    input_check.py

DESCRIPTION:
    This module checks that the input data is valid and within limits.

    The purpose of this module is to ensure that 1) all the user input data
    is physically valid, e.g., a weight can't be negative, and 2) the data
    is within the expected limits, e.g., the usable fuel can't be higher
    than 50 gallons.
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


def check_basic_weight(basic_weight):
    """
    Returns None if the argument is a valid basic empty weight,
    otherwise the program stops with a custom error message.
    """
    if check_if_value_is_numeric(basic_weight) is False:
        sys.exit('Basic weight | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(basic_weight) is True:
        sys.exit('Basic weight | ' + msg_error_negative_value)
    elif int(basic_weight) < 1397 or int(basic_weight) > 2300:
        sys.exit('Basic weight | ERROR: The weight must be between 1397 and 2300 pounds.')
    else:
        return None


def check_basic_moment(basic_moment):
    """
    Returns None if the argument is a valid basic moment,
    otherwise the program stops with a custom error message.
    """
    if check_if_value_is_numeric(basic_moment) is False:
        sys.exit('Basic moment | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(basic_moment) is True:
        sys.exit('Basic moment | ' + msg_error_negative_value)
    elif int(basic_moment) < 0 or int(basic_moment) > 120:
        sys.exit('Basic moment | ERROR: The moment must be between 0 and 120 lb-in (/1000).')
    else:
        return None


def check_usable_fuel(usable_fuel):
    """
    Returns None if the argument is a valid fuel volume,
    otherwise the program stops with a custom error message.
    """
    if check_if_value_is_numeric(usable_fuel) is False:
        sys.exit('Usable fuel | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(usable_fuel) is True:
        sys.exit('Usable fuel | ' + msg_error_negative_value)
    elif int(usable_fuel) < 0 or int(usable_fuel) > 50:
        sys.exit('Usable fuel | ERROR: The usable fuel must be between 0 and 50 gallons.')
    else:
        return None


def check_person_weight(weight):
    """
    Returns None if the argument is a valid person weight,
    otherwise the program stops with a custom error message.
    """
    if check_if_value_is_numeric(weight) is False:
        sys.exit('Person weight | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(weight) is True:
        sys.exit('Person weight | ' + msg_error_negative_value)
    elif int(weight) < 0 or int(weight) > 400:
        sys.exit('Person weight | ERROR: The person weight must be between 0 and 400 pounds.')
    else:
        return None


def check_cargo_1(cargo_1):
    """
    Returns None if the argument is a valid cargo weight,
    otherwise the program stops with a custom error message.
    """
    if check_if_value_is_numeric(cargo_1) is False:
        sys.exit('Baggage area 1t | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(cargo_1) is True:
        sys.exit('Baggage area 1 | ' + msg_error_negative_value)
    elif int(cargo_1) < 0 or int(cargo_1) > 120:
        sys.exit('Baggage area 1 | ERROR: The weight must be between 0 and 120 pounds.')
    else:
        return None


def check_cargo_2(cargo_2):
    """
    Returns None if the argument is a valid cargo weight,
    otherwise the program stops with a custom error message.
    """
    if check_if_value_is_numeric(cargo_2) is False:
        sys.exit('Baggage area 2 | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(cargo_2) is True:
        sys.exit('Baggage area 2 | ' + msg_error_negative_value)
    elif int(cargo_2) < 0 or int(cargo_2) > 50:
        sys.exit('Baggage area 2 | ERROR: The weight must be between 0 and 50 pounds.')
    else:
        return None


def check_fuel_allowance(fuel_allowance):
    """
    Returns None if the argument is a valid fuel allowance weight,
    otherwise the program stops with a custom error message.
    """
    if check_if_value_is_numeric(fuel_allowance) is False:
        sys.exit('Fuel allowance | ' + msg_error_invalid_value)
    elif check_if_value_is_negative(fuel_allowance) is True:
        sys.exit('Fuel allowance | ' + msg_error_negative_value)
    elif int(fuel_allowance) < 0 or int(fuel_allowance) > 150:
        sys.exit('Fuel allowance | ERROR: The fuel weight must be between 0 and 150 pounds.')
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
    check_basic_weight(input_data['basic_weight'])
    check_basic_moment(input_data['basic_moment'])
    # Check weight data.
    check_usable_fuel(input_data['usable_fuel'])
    check_person_weight(input_data['pilot'])
    check_person_weight(input_data['front_pax'])
    check_person_weight(input_data['rear_pax_1'])
    check_person_weight(input_data['rear_pax_2'])
    check_cargo_1(input_data['cargo_1'])
    check_cargo_2(input_data['cargo_2'])
    check_fuel_allowance(input_data['fuel_allowance'])
    return input_data
