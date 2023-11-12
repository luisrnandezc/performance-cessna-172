"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023
"""

import sys


def interpolate(x1, y1, x2, y2, xi):
    """Returns the interpolated value yi."""
    yi = round(((xi-x2)*y1 - (xi-x1)*y2)/(x1-x2), 2)
    return yi


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
    if delta_temp < -10:
        std_temp_diff = 'isa_m20'
    elif delta_temp > 10:
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
    altitude_values = list(range(0, 14000, 2000))
    power_values = [45, 55, 65, 75]
    if press_alt in altitude_values and power in power_values:
        value = df.loc[press_alt][str(power)]
    elif press_alt in altitude_values and power not in power_values:
        power_values.append(power)
        power_values.sort()
        index = power_values.index(power)
        low_power = power_values[index - 1]
        high_power = power_values[index + 1]
        low_power_endurance = df.loc[press_alt][str(low_power)]
        high_power_endurance = df.loc[press_alt][str(high_power)]
        value = interpolate(low_power, low_power_endurance, high_power, high_power_endurance, power)
    elif press_alt not in altitude_values and power in power_values:
        altitude_values.append(press_alt)
        altitude_values.sort()
        index = altitude_values.index(press_alt)
        low_altitude = altitude_values[index - 1]
        high_altitude = altitude_values[index + 1]
        low_altitude_endurance = df.loc[low_altitude][str(power)]
        high_altitude_endurance = df.loc[high_altitude][str(power)]
        value = interpolate(low_altitude, low_altitude_endurance, high_altitude, high_altitude_endurance, press_alt)
    else:
        # Data preparation for interpolation.
        power_values.append(power)
        power_values.sort()
        power_index = power_values.index(power)
        low_power = power_values[power_index - 1]
        high_power = power_values[power_index + 1]
        altitude_values.append(press_alt)
        altitude_values.sort()
        alt_index = altitude_values.index(press_alt)
        low_altitude = altitude_values[alt_index - 1]
        high_altitude = altitude_values[alt_index + 1]
        # First is necessary to interpolate for both the low and high altitudes values.
        low_alt_low_power_endurance = df.loc[low_altitude][str(low_power)]
        low_alt_high_power_endurance = df.loc[low_altitude][str(high_power)]
        low_alt_endurance = interpolate(low_power, low_alt_low_power_endurance, high_power, low_alt_high_power_endurance, power)
        high_alt_low_power_endurance = df.loc[high_altitude][str(low_power)]
        high_alt_high_power_endurance = df.loc[high_altitude][str(high_power)]
        high_alt_endurance = interpolate(low_power, high_alt_low_power_endurance, high_power, high_alt_high_power_endurance, power)
        # Now we can compute the final interpolated value for the real altitude.
        value = interpolate(low_altitude, low_alt_endurance, high_altitude, high_alt_endurance, press_alt)
    return value


def range_wind_correction(wind, endurance, max_range):
    if wind != 0:
        wind_velocity = int(wind[0:2])
        wind_direction = wind[-1]
        corr = endurance*wind_velocity
        if wind_direction == 'T':
            max_range = max_range + corr
        else:
            max_range = max_range - corr
    return int(round(max_range, 0))


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
    max_endurance = round(compute_endurance(press_alt_500, power, endurance_df), 1)
    max_range = round(compute_range(press_alt_500, power, range_df), 0)
    # Range correction because of wind.
    max_range = range_wind_correction(input_data['CRW'], max_endurance, max_range)
    return max_endurance, max_range, velocity, fuel_flow
