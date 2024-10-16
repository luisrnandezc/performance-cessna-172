from . import input_check
from . import compute


def compute_weight_and_balance(input_data):

    # Check input data.
    input_data = input_check.check_input_data(input_data)

    # Compute weight and balance data.
    balance_data = compute.compute_weight_and_balance(input_data)

    return balance_data


if __name__ == '__main__':
    # TODO: add testing functionality.
    print("Run directly")
