"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luishc1618
Date: 13/09/2023
"""


def write_output_file(results_values):
    results_keys = ['TOGR', 'TOGR50', 'END', 'RAN', 'FRQ', 'FR', 'LDGR', 'LDGR50']
    results = {}
    for (key, value) in zip(results_keys, results_values):
        results[key] = value
    return results

