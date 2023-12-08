"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
"""

import sys
import helpers


def compute_standard_temperature_difference(press_alt, temp):
    """Returns the temperature difference between the cruise temperature
    and the expected standard temperature at cruise altitude.

   Three possible return values:

        'isa_m20': the cruise temperature is ISA-20.
        'isa_p20': the cruise temperature is ISA+20.
        'isa': the cruise temperature is ISA+0.

    Args:
        press_alt (int): cruise pressure altitude.
        temp (int): cruise temperature.

    Returns:
        std_temp_diff (str): difference between cruise and standard temperature.
    """
    std_temp = int(round(-0.002*press_alt + 15, 0))   # Linear equation representing the variation of temperature with pressure altitude.
    delta_temp = temp - std_temp
    if delta_temp <= -10:
        std_temp_diff = 'isa_m20'
    elif delta_temp >= 10:
        std_temp_diff = 'isa_p20'
    else:
        std_temp_diff = 'isa'
    return std_temp_diff


def check_for_invalid_data(power_press_alt, rpm):
    """Checks for invalid combinations of RPM and Pressure Altitude"""
    invalid_combinations = [(2000, 2500), (4000, 2550), (6000, 2600), (8000, 2650)]
    data = (power_press_alt, rpm)
    if data in invalid_combinations:
        sys.exit('ERROR: las RPM seleccionadas exceden el valor máximo para la altitud de crucero.')
    return None


def compute_cruise_power_setting(power_df, press_alt, rpm, std_temp_difference):
    """Returns the engine power setting for cruise flight

    Args:
        power_df: cruise power setting dataframe.
        press_alt (int): cruise pressure altitude.
        rpm (int): cruise RPM selected by the pilot.
        std_temp_difference (str): difference between cruise and standard temperature.

    Returns:
        power (int): cruise engine power in BHP.
        velocity (int): cruise velocity in knots.
        fuel_flow (float): cruise fuel flow in gph.
    """
    power_df = power_df[(power_df['press_alt'] == press_alt) & (power_df['rpm'] == rpm)]
    power = int(power_df.iloc[0][std_temp_difference + '_bhp'])
    velocity = int(power_df.iloc[0][std_temp_difference + '_ktas'])
    fuel_flow = power_df.iloc[0][std_temp_difference + '_gph']
    return power, velocity, fuel_flow


def compute_endurance(press_alt, power, df):
    """Returns the aircraft endurance in hours.

    Args:
        press_alt (int): cruise pressure altitude.
        power (int): cruise power setting.
        df: endurance dataframe.

    Returns:
        endurance (float): aircraft flight endurance in hours.
    """
    try:
        endurance = df.loc[press_alt][str(power)]
    except KeyError:
        endurance = helpers.dataframe_interpolation(press_alt, power, df)
    return round(endurance, 2)


def compute_range(press_alt, power, df):
    """Returns the aircraft range in nautical miles.

    Args:
        press_alt (int): cruise pressure altitude.
        power (int): cruise power setting.
        df: range dataframe.

    Returns:
        rang (float): aircraft flight range in nautical miles.
    """
    try:
        rang = df.loc[press_alt][str(power)]
    except KeyError:
        rang = helpers.dataframe_interpolation(press_alt, power, df)
    return round(rang, 0)


def range_wind_correction(wind, endurance, max_range):
    """Returns the aircraft range corrected by wind.

    Args:
        wind (str): cruise wind velocity and direction.
        endurance (float): aircraft flight endurance in hours.
        max_range (float): aircraft flight range in nautical miles.

    Returns:
        max_range (int): corrected aircraft flight range in nautical miles.
    """
    if wind != 0:
        wind_velocity = int(wind[0:2])
        wind_direction = wind[-1]
        corr = endurance*wind_velocity
        if wind_direction == 'T':
            max_range = int(round(max_range + corr, 0))
        else:
            max_range = int(round(max_range - corr, 0))
    return max_range


def compute_cruise_performance(input_data, power_df, range_df, endurance_df):
    press_alt_500 = input_data['CRPA5']
    press_alt_1000 = input_data['CRPA10']
    temp = input_data['CRT']
    # Compute standard temperature difference.
    std_temp_difference = compute_standard_temperature_difference(press_alt_1000, temp)
    # Compute values required by the cruise power setting table.
    power_press_alt = input_data['CRPPA']
    rpm = input_data['RPM']
    # Checks for invalid combinations of RPM and pressure altitude
    if std_temp_difference == 'isa_m20':
        check_for_invalid_data(power_press_alt, rpm)
    # Read the power setting from the table.
    power, velocity, fuel_flow = compute_cruise_power_setting(power_df, power_press_alt, rpm, std_temp_difference)
    # Compute the total endurance and range.
    max_endurance = compute_endurance(press_alt_500, power, endurance_df)
    max_range = compute_range(press_alt_500, power, range_df)
    # Range correction because of wind.
    max_range = range_wind_correction(input_data['CRW'], max_endurance, max_range)
    return max_endurance, max_range, velocity, fuel_flow
