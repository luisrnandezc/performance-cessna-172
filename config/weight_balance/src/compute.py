

def compute_takeoff_weight(data):
    keys = ['basic_weight', 'pilot', 'front_pax', 'rear_pax_left', 'rear_pax_right', 'cargo_1', 'cargo_2']
    takeoff_weight = 0
    for key in keys:
        takeoff_weight = takeoff_weight + data[key]
    return takeoff_weight + 6*data['usable_fuel'] - data['fuel_allowance']


def compute_takeoff_cg_moment(data):
    return None


def compute_takeoff_cg_location(data):
    return None


def compute_weight_and_balance(input_data):

    balance_data = {}
    return balance_data
