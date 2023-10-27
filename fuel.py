"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luishc1618
Date: 13/09/2023
"""


def compute_climb_time(press_alt, df):
    time = df.loc[press_alt]['time']
    return time


def compute_climb_fuel(press_alt, df):
    fuel = df.loc[press_alt]['fuel']
    return fuel


def compute_climb_distance(press_alt, df):
    distance = df.loc[press_alt]['distance']
    return distance


def apply_temperature_correction(time, fuel, distance, press_alt, temp, df):
    std_temp = df.loc[press_alt]['temp']
    delta_temp = temp - std_temp
    if delta_temp > 0:
        correction = round(delta_temp/100, 2)
        time = time*(1 + correction)
        fuel = fuel*(1 + correction)
        distance = distance*(1 + correction)
    return time, fuel, distance


def compute_climb_data(press_alt, temp, df):
    time = compute_climb_time(press_alt, df)
    fuel = compute_climb_fuel(press_alt, df)
    distance = compute_climb_distance(press_alt, df)
    time, fuel, distance = apply_temperature_correction(time, fuel, distance, press_alt, temp, df)
    return time, fuel, distance


def compute_ground_speed(velocity, wind):
    if wind[-1] == 'H':
        ground_speed = velocity - int(wind[0:2])
    else:
        ground_speed = velocity + int(wind[0:2])
    return ground_speed


def compute_fuel_required(input_data, climb_df, velocity, fuel_flow):
    # First we need to compute the time, fuel and distance to climb from SL.
    takeoff_press_alt = input_data['TOPA']
    takeoff_temp = input_data['RTOT']
    takeoff_climb_data = compute_climb_data(takeoff_press_alt, takeoff_temp, climb_df)
    cruise_press_alt = input_data['CRPA10']
    cruise_temp = input_data['CRT']
    cruise_climb_data = compute_climb_data(cruise_press_alt, cruise_temp, climb_df)
    # Now the climb data from takeoff to cruise altitude can be computed.
    climb_data = tuple(map(lambda i, j: round(i - j, 1), cruise_climb_data, takeoff_climb_data))
    # Computation of the total fuel required.
    cruise_distance = int(round(input_data['TD'] - climb_data[2], 0))
    ground_speed = compute_ground_speed(velocity, input_data['CRW'])
    # The cruise time can be now computed using the cruise distance and the ground speed.
    cruise_time = round(cruise_distance/ground_speed, 1)
    # Finally, the total fuel consumption is computed.
    cruise_fuel = round(cruise_time*fuel_flow, 1)
    total_fuel_required = 1.1 + climb_data[1] + cruise_fuel
    fuel_reserve = round(input_data['FC'] - total_fuel_required, 1)
    return total_fuel_required, fuel_reserve
