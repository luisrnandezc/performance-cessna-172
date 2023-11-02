"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023
"""

text_for_file = ['Takeoff ground roll: ',
                 'Takeoff ground roll 50 ft obstacle: ',
                 'Endurance: ',
                 'Range: ',
                 'Fuel required: ',
                 'Fuel reserve: ',
                 'Landing ground roll: ',
                 'Landing ground roll 50 ft obstacle: ']


def organize_final_results(results_values):
    results_keys = ['TOGR', 'TOGR50', 'END', 'RAN', 'FRQ', 'FR', 'LDGR', 'LDGR50']
    results = {}
    for (key, value) in zip(results_keys, results_values):
        results[key] = value
    return results


def generate_text_file(text, results):
    # TODO
    return None


def write_output_file(results_values):
    results = organize_final_results(results_values)
    # file = generate_text_file(text_for_file, results)
    return None
