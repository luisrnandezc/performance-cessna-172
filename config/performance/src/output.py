"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023
"""


def organize_final_results(values):
    """Returns a dictionary with the calculated performance values.

    Args:
        values: list containing the performance values.

    Returns:
        results: dictionary containing the performance values.
    """
    keys = ['TOGR [ft]', 'TOGR50 [ft]',
            'Endurance [hours]', 'Range [nm]', 'Fuel [gal]', 'Reserve [gal]',
            'LDGR [ft]', 'LDGR50 [ft]']
    results = {}
    for (key, value) in zip(keys, values):
        results[key] = value
    return results


def write_output_file(results, path):
    """Generates a .txt file with the calculated performance values.

    Args:
        results: list containing the performance values.
        path: output path for the .txt file.

    Returns:
        None
    """
    results = organize_final_results(results)
    with open(path + '\\' + 'output.txt', 'w') as f:
        for key, value in results.items():
            f.write('%s: %s\n' % (key, value))
    return None
