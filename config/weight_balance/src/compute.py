

def compute_takeoff_weight(data):
    keys = ['basic_weight', 'pilot', 'front_pax', 'rear_pax_left', 'rear_pax_right', 'cargo_1', 'cargo_2']
    takeoff_weight = 0
    for key in keys:
        takeoff_weight = takeoff_weight + data[key]
    return takeoff_weight + 6*data['usable_fuel'] - 6*data['fuel_allowance']


def compute_valid_arms(data):
    arms_data = {
        '0': [37, 37, 73, 73, 95, 95, 123],
        '1': [37, 37, 73, 73, 96, 96, 123]
    }
    valid_arms = arms_data[str(data['seat_config'])]
    return valid_arms


def compute_fuel_moment(fuel_volume):
    fuel_weight = fuel_volume*6  # 1 gallon of AvGas weights approx. 6 pounds.
    return round((fuel_weight*12/250), 1)


def compute_takeoff_moment(data, arms):
    keys = ['pilot', 'front_pax', 'rear_pax_left', 'rear_pax_right', 'cargo_1', 'cargo_2']
    weights_moment = 0
    for (key, arm) in zip(keys, arms):
        weights_moment = weights_moment + data[key]*arm
    fuel_moment = compute_fuel_moment(data['usable_fuel'])
    fuel_allowance_moment = compute_fuel_moment(data['fuel_allowance'])
    takeoff_moment = data['basic_moment'] + round((weights_moment/1000), 1) + fuel_moment - fuel_allowance_moment
    return round(takeoff_moment, 1)


def compute_takeoff_cg_location(weight, moment):
    return round((moment/weight)*1000, 1)


def compute_weight_and_balance(input_data):
    takeoff_weight = compute_takeoff_weight(input_data)
    arms = compute_valid_arms(input_data)
    takeoff_moment = compute_takeoff_moment(input_data, arms)
    cg_location = compute_takeoff_cg_location(takeoff_weight, takeoff_moment)
    balance_data = {
        'takeoff_weight': takeoff_weight,
        'takeoff_moment': takeoff_moment,
        'cg_location': cg_location,
        'condition': None
    }
    return balance_data
