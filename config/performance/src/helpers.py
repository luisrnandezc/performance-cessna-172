"""
Cessna 172N Performance Calculator
Author: Luis Hernández
GitHub: luisrnandezc
Date: 13/09/2023
"""

import bisect


def linear_interpolation(x1, y1, x2, y2, xi):
    """Returns the interpolated value yi."""
    yi = round(((xi - x2) * y1 - (xi - x1) * y2) / (x1 - x2), 2)
    return yi


def compute_sorted_index(values, v):
    """Returns the correct index of v when inserted in values."""
    bisect.insort(values, v)
    return values.index(v)


def dataframe_interpolation(row, column, df):
    """Returns the dataframe value located at the position [row][column].

    If the row or/and column are not present in the dataframe the value
    is estimated by means of interpolation.

    Args:
        row (int): cruise pressure altitude in feets.
        column (int): cruise power setting in % (e.g. 65 = 65%).
        df: performance dataframe.

    Returns:
        interpolated_value (float): dataframe value located at [row][column].
    """
    row_indices = df.index.tolist()
    column_names = list(reversed([int(i) for i in df.columns.tolist()]))
    if row in row_indices and column not in column_names:
        index = compute_sorted_index(column_names, column)
        prev_col = column_names[index - 1]
        next_col = column_names[index + 1]
        prev_col_value = df.loc[row][str(prev_col)]
        next_col_value = df.loc[row][str(next_col)]
        interpolated_value = linear_interpolation(prev_col, prev_col_value, next_col, next_col_value, column)
        return interpolated_value
    elif row not in row_indices and column in column_names:
        index = compute_sorted_index(row_indices, row)
        prev_row = row_indices[index - 1]
        next_row = row_indices[index + 1]
        prev_row_value = df.loc[prev_row][str(column)]
        next_row_value = df.loc[next_row][str(column)]
        interpolated_value = linear_interpolation(prev_row, prev_row_value, next_row, next_row_value, row)
        return interpolated_value
    else:
        # If both the row and column are not present in the dataframe, then a
        # bilinear interpolation is required.
        col_index = compute_sorted_index(column_names, column)
        prev_col = column_names[col_index - 1]
        next_col = column_names[col_index + 1]
        row_index = compute_sorted_index(row_indices, row)
        prev_row = row_indices[row_index - 1]
        next_row = row_indices[row_index + 1]
        # Interpolation for the previous row and the unknown column.
        prev_col_prev_row = df.loc[prev_row][str(prev_col)]
        next_col_prev_row = df.loc[prev_row][str(next_col)]
        prev_row_value = linear_interpolation(prev_col, prev_col_prev_row, next_col, next_col_prev_row, column)
        # Interpolation for the next row and the unknown column.
        prev_col_next_row = df.loc[next_row][str(prev_col)]
        next_col_next_row = df.loc[next_row][str(next_col)]
        next_row_value = linear_interpolation(prev_col, prev_col_next_row, next_col, next_col_next_row, column)
        # Final interpolation using the values for the unknown column.
        interpolated_value = linear_interpolation(prev_row, prev_row_value, next_row, next_row_value, row)
        return interpolated_value
