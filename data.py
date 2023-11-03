"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023

NAME:
    data.py

DESCRIPTION:
    The objective of this module is to compute the valid performance values
    that can be used to extract data from the performance
    tables. This is required because the performance tables have data only
    for a set of specific conditions, so it may be necessary to approximate
    the user specified value to a value present in the tables.

EXAMPLE:
    The takeoff performance table only has data for the valid altitudes
    between 0 and 12000 feets (in 1000 feets increments, i.e., 0, 1000,
    2000,..., 8000). If the user specified altitude is not one of these
    values, it is necessary to approximate the value in accordance with
    the following criteria:

    > Suppose the user specified altitude X is between two valid altitudes A and B (A < X < B).
    > If X < A + 250 ft, the altitude is approximated to A.
    > If X >= A + 250 ft, the altitude is approximated to B.

    If the user altitude is 1250 ft, the returned valid altitude would be
    2000 ft, not 1000 ft. Considering that aircraft takeoff performance
    reduces with altitude, by using 250 ft instead of 500 ft as the
    approximation threshold, the procedure yields a more conservative
    result. A similar procedure is employed to compute the rest of the
    valid data (weight, temperature and rpm).
"""


def valid_takeoff_weight(takeoff_weight):
    """Returns the corrected takeoff weight."""
    if takeoff_weight <= 1900:
        return 1900
    elif takeoff_weight <= 2100:
        return 2100
    else:
        return 2300


def valid_takeoff_press_alt(takeoff_press_alt):
    """Returns the corrected takeoff pressure altitude."""
    valid_altitudes = list(range(0, 9000, 1000))
    max_alt = valid_altitudes[-1]
    if takeoff_press_alt > max_alt:
        return max_alt
    for valid_alt in valid_altitudes:
        if takeoff_press_alt == valid_alt:
            return valid_alt
        elif takeoff_press_alt >= valid_alt + 250:
            continue
        else:
            return valid_alt


def valid_takeoff_temp(takeoff_temp):
    """Returns the corrected takeoff temperature."""
    valid_temperatures = list(range(0, 50, 10))
    min_temp = valid_temperatures[0]
    if takeoff_temp < min_temp:
        return min_temp
    for valid_temp in valid_temperatures:
        if takeoff_temp == valid_temp:
            return takeoff_temp
        elif takeoff_temp >= valid_temp + 4:
            continue
        else:
            return valid_temp


def valid_roc_press_alt(takeoff_press_alt):
    """Returns the corrected pressure altitude for ROC computation.

    The objective of this function is to find the pressure altitude
    that can be used to read the Rate of Climb (ROC) value from
    the ROC table. This is required because the ROC table only
    has data for altitude values from 0 to 12000 feets in 2000 feets
    increments.

    The takeoff_press_alt is rounded to the next valid altitude when
    the former is 500 feets higher or more than the current valid
    altitude. Please see the following examples:

        > If takeoff_press_alt is equal to 2200 ft, the function
        returns 2000 ft as the valid pressure altitude.
        > If takeoff_press_alt is equal to 2500 ft, the function
        returns 4000 ft as the valid pressure altitude.
        > If takeoff_press_alt is equal to 3000 ft, the function
        returns 4000 ft as the valid pressure altitude.

    Args:
        takeoff_press_alt: takeoff pressure altitude [ft]
    Returns:
        valid_alt: valid ROC pressure altitude [ft]
    """
    valid_altitudes = list(range(0, 14000, 2000))
    max_alt = valid_altitudes[-1]
    if takeoff_press_alt > max_alt:
        return max_alt
    for valid_alt in valid_altitudes:
        if takeoff_press_alt == valid_alt:
            return valid_alt
        elif takeoff_press_alt >= valid_alt + 500:
            continue
        else:
            return valid_alt


def valid_roc_temp(takeoff_temp):
    """Returns the corrected temperature for ROC computation."""
    valid_temperatures = list(range(-20, 60, 20))
    min_temp = valid_temperatures[0]
    if takeoff_temp < min_temp:
        return min_temp
    for valid_temp in valid_temperatures:
        if takeoff_temp == valid_temp:
            return takeoff_temp
        elif takeoff_temp >= valid_temp + 5:
            continue
        else:
            return valid_temp


def valid_cruise_press_alt_500(cruise_press_alt):
    """Returns the corrected pressure altitude required
     for endurance and range calculation.
    """
    valid_altitudes = list(range(0, 13000, 500))
    max_alt = valid_altitudes[-1]
    if cruise_press_alt > max_alt:
        return max_alt
    else:
        for valid_alt in valid_altitudes:
            if cruise_press_alt == valid_alt:
                return valid_alt
            elif cruise_press_alt >= valid_alt + 250:
                continue
            else:
                return valid_alt


def valid_cruise_press_alt_1000(cruise_press_alt):
    """Returns the corrected pressure altitude required
     for climb performance computation.
    """
    valid_altitudes = list(range(0, 13000, 1000))
    max_alt = valid_altitudes[-1]
    if cruise_press_alt > max_alt:
        return max_alt
    else:
        for valid_alt in valid_altitudes:
            if cruise_press_alt == valid_alt:
                return valid_alt
            elif cruise_press_alt >= valid_alt + 250:
                continue
            else:
                return valid_alt


def valid_cruise_power_press_alt(cruise_press_alt):
    """Returns the corrected pressure altitude required
     for cruise power calculation.
    """
    valid_altitudes = list(range(2000, 14000, 2000))
    max_alt = valid_altitudes[-1]
    if cruise_press_alt > max_alt:
        return max_alt
    else:
        for valid_alt in valid_altitudes:
            if cruise_press_alt == valid_alt:
                return valid_alt
            elif cruise_press_alt >= valid_alt + 500:
                continue
            else:
                return valid_alt


def compute_valid_rpm_for_cruise_altitudes(power_df):
    valid_rpm = {}
    valid_altitudes = list(range(2000, 14000, 2000))
    for press_alt in valid_altitudes:
        valid_rpm[press_alt] = power_df[(power_df['press_alt'] == press_alt)]['rpm'].values.tolist()
    return valid_rpm


def valid_cruise_rpm(power_df, cruise_power_press_alt, cruise_rpm):
    valid_rpm_for_cruise_altitudes = compute_valid_rpm_for_cruise_altitudes(power_df)
    rpm_values = valid_rpm_for_cruise_altitudes[cruise_power_press_alt]
    rpm_values.append(cruise_rpm)
    rpm_values.sort()
    rpm_index = rpm_values.index(cruise_rpm)
    low_rpm = rpm_values[rpm_index-1]
    high_rpm = rpm_values[rpm_index+1]
    low_delta = cruise_rpm - low_rpm
    high_delta = high_rpm - cruise_rpm
    if low_delta < high_delta:
        return low_rpm
    elif low_delta > high_delta:
        return high_rpm
    else:
        return high_rpm


def valid_landing_press_alt(landing_press_alt):
    valid_altitudes = list(range(0, 9000, 1000))
    max_alt = valid_altitudes[-1]
    if landing_press_alt > max_alt:
        return max_alt
    for valid_alt in valid_altitudes:
        if landing_press_alt == valid_alt:
            return valid_alt
        elif landing_press_alt >= valid_alt + 250:
            continue
        else:
            return valid_alt


def valid_landing_temp(landing_temp):
    valid_temperatures = list(range(0, 50, 10))
    min_temp = valid_temperatures[0]
    if landing_temp < min_temp:
        return min_temp
    for valid_temp in valid_temperatures:
        if landing_temp == valid_temp:
            return landing_temp
        elif landing_temp >= valid_temp + 4:
            continue
        else:
            return valid_temp


def update_input_data(input_data, data_to_update, values_to_update):
    for (key, value) in zip(data_to_update, values_to_update):
        input_data[key] = value
    return input_data


def convert_to_integer(input_data):
    for data in input_data:
        value = input_data[data]
        if type(value) == str and value.isnumeric() is True:
            input_data[data] = int(value)
    return input_data


def compute_valid_performance_data(input_data, power_df):
    # Takeoff data.
    takeoff_weight = valid_takeoff_weight(int(input_data['TOWG']))
    takeoff_press_alt = valid_takeoff_press_alt(int(input_data['TOPA']))
    takeoff_temp = valid_takeoff_temp(int(input_data['TOT']))
    real_takeoff_temp = int(input_data['TOT'])
    # Climb data.
    roc_press_alt = valid_roc_press_alt(int(input_data['TOPA']))
    roc_temp = valid_roc_temp(int(input_data['TOT']))
    # Cruise data.
    real_press_alt = int(input_data['CRPA'])
    cruise_press_alt_500 = valid_cruise_press_alt_500(real_press_alt)
    cruise_press_alt_1000 = valid_cruise_press_alt_1000(real_press_alt)
    cruise_power_press_alt = valid_cruise_power_press_alt(real_press_alt)
    cruise_rpm = valid_cruise_rpm(power_df, cruise_power_press_alt, int(input_data['RPM']))
    # Landing data.
    landing_press_alt = valid_landing_press_alt(int(input_data['LDPA']))
    landing_temp = valid_landing_temp(int(input_data['LDT']))
    # Update the original input data with the validated data.
    data_to_update = ['TOWG', 'TOPA', 'TOT', 'RTOT', 'ROCPA', 'ROCT', 'CRPA5', 'CRPA10', 'CRPPA', 'RPM', 'LDPA', 'LDT']
    values_to_update = [takeoff_weight, takeoff_press_alt, takeoff_temp, real_takeoff_temp, roc_press_alt, roc_temp,
                        cruise_press_alt_500, cruise_press_alt_1000, cruise_power_press_alt, cruise_rpm,
                        landing_press_alt, landing_temp]
    input_data = update_input_data(input_data, data_to_update, values_to_update)
    # Convert the corresponding data from string to integer.
    input_data = convert_to_integer(input_data)
    return input_data
