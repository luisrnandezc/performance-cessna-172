"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023
"""


def organize_final_results(results_values):
    results_keys = ['TOGR [ft]', 'TOGR50 [ft]', 'Endurance [hours]', 'Range [nm]', 'Fuel [gal]', 'Reserve [gal]', 'LDGR [ft]', 'LDGR50 [ft]']
    results = {}
    for (key, value) in zip(results_keys, results_values):
        results[key] = value
    return results


def generate_text_file(results):
    with open(r'C:\Users\luish\Desktop\Projects\Performance Cessna 172N\output\output.txt', 'w') as f:
        for key, value in results.items():
            f.write('%s: %s\n' % (key, value))
    return None


def write_output_file(results_values):
    results = organize_final_results(results_values)
    generate_text_file(results)
    return None
