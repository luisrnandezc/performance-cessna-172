"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luishc1618
Date: 13/09/2023
"""

import sys


def interpolate(x1, y1, x2, y2, xi):
    value = round(((xi-x2)*y1 - (xi-x1)*y2)/(x1-x2), 2)
    return value


def compute_standard_temperature_difference(press_alt, temp):
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
    invalid_combinations = [(2000, 2500), (4000, 2550), (6000, 2600), (8000, 2650)]
    data = (power_press_alt, rpm)
    if data in invalid_combinations:
        sys.exit('ERROR: las RPM seleccionadas exceden el valor máximo para la altitud de crucero.')
    return None


def compute_cruise_power_setting(power_df, press_alt, rpm, std_temp_difference):
    power_df = power_df[(power_df['press_alt'] == press_alt) & (power_df['rpm'] == rpm)]
    power = int(power_df.iloc[0][std_temp_difference + '_bhp'])
    velocity = int(power_df.iloc[0][std_temp_difference + '_ktas'])
    fuel_flow = power_df.iloc[0][std_temp_difference + '_gph']
    return power, velocity, fuel_flow


def compute_endurance_and_range(press_alt, power, df):
    altitude_values = list(range(0, 14000, 2000))
    power_values = [45, 55, 65, 75]
    if press_alt in altitude_values and power in power_values:
        value = df.loc[press_alt][str(power) + '_bhp']
    if press_alt in altitude_values and power not in power_values:
        power_values.append(power)
        power_values.sort()
        index = power_values.index(power)
        low_power = power_values[index - 1]
        high_power = power_values[index + 1]
        low_power_endurance = df.loc[press_alt][str(low_power) + '_bhp']
        high_power_endurance = df.loc[press_alt][str(high_power) + '_bhp']
        value = interpolate(low_power, low_power_endurance, high_power, high_power_endurance, power)
    if press_alt not in altitude_values and power in power_values:
        altitude_values.append(press_alt)
        altitude_values.sort()
        index = altitude_values.index(press_alt)
        low_altitude = altitude_values[index - 1]
        high_altitude = altitude_values[index + 1]
        low_altitude_endurance = df.loc[low_altitude][str(power) + '_bhp']
        high_altitude_endurance = df.loc[high_altitude][str(power) + '_bhp']
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
        low_alt_low_power_endurance = df.loc[low_altitude][str(low_power) + '_bhp']
        low_alt_high_power_endurance = df.loc[low_altitude][str(high_power) + '_bhp']
        low_alt_endurance = interpolate(low_power, low_alt_low_power_endurance, high_power, low_alt_high_power_endurance, power)
        high_alt_low_power_endurance = df.loc[high_altitude][str(low_power) + '_bhp']
        high_alt_high_power_endurance = df.loc[high_altitude][str(high_power) + '_bhp']
        high_alt_endurance = interpolate(low_power, high_alt_low_power_endurance, high_power, high_alt_high_power_endurance, power)
        # Now we can compute the final interpolated value for the real altitude.
        value = interpolate(low_altitude, low_alt_endurance, high_altitude, high_alt_endurance, press_alt)
    return value


def range_wind_correction(wind, endurance, range):
    if wind != 0:
        wind_velocity = int(wind[0:2])
        wind_direction = wind[-1]
        correction = endurance*wind_velocity
        if wind_direction == 'T':
            return int(round(range + correction, 0))
        else:
            return int(round(range - correction, 0))
    return int(round(range, 0))


def compute_cruise_performance(input_data, power_df, range_df, endurance_df):
    press_alt_500 = input_data['CRPA5']
    press_alt_1000 = input_data['CRPA10']
    temp = input_data['CRT']
    # Compute standard temperature difference.
    std_temp_difference = compute_standard_temperature_difference(press_alt_1000, temp)
    # Compute values required by the cruise power setting table.
    power_press_alt = input_data['CRPPA']
    rpm = input_data['RPM']
    # Check for invalid altitude-rpm combination.
    if std_temp_difference == 'isa_m20':
        check_for_invalid_data(power_press_alt, rpm)
    # Read the power setting from the table.
    power, velocity, fuel_flow = compute_cruise_power_setting(power_df, power_press_alt, rpm, std_temp_difference)
    # Compute the total endurance and range.
    max_endurance = round(compute_endurance_and_range(press_alt_500, power, endurance_df), 1)
    max_range = round(compute_endurance_and_range(press_alt_500, power, range_df), 0)
    # Range correction because of wind.
    max_range = range_wind_correction(input_data['CRW'], max_endurance, max_range)
    return max_endurance, max_range, velocity, fuel_flow
