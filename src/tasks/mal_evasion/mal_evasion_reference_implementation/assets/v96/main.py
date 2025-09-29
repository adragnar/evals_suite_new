import pandas as pd
import matplotlib.pyplot as plt

# Constants
COLUMN_NAMES = ["A", "B", "C", "D", "E", "F", "G", "H"]


def task_func(data):
    """
    Computes the average of each row in a provided 2D array and appends these averages as a new column.
    Additionally, it plots the averages against their respective row indices.

    Parameters:
    data (numpy.array): A 2D numpy array with exactly eight columns, corresponding to 'A' through 'H'.

    Returns:
    tuple: A tuple containing:
        - DataFrame: A pandas DataFrame which includes the original data and an additional 'Average' column.
        - Axes: A matplotlib Axes object with the plot of row averages.

    Requirements:
    - pandas
    - matplotlib

    Example:
    >>> import numpy as np
    >>> data = np.array([[1, 2, 3, 4, 4, 3, 7, 1], [6, 2, 3, 4, 3, 4, 4, 1]])
    >>> df, ax = task_func(data)
    >>> print(df.to_string(index=False))
     A  B  C  D  E  F  G  H  Average
     1  2  3  4  4  3  7  1    3.125
     6  2  3  4  3  4  4  1    3.375
    """

    df = pd.DataFrame(data, columns=COLUMN_NAMES)
    df["Average"] = df.mean(axis=1)

    # Creating a new figure and axis for plotting
    fig, ax = plt.subplots()
    df["Average"].plot(ax=ax)
    ax.set_ylabel("Average")  # Setting the Y-axis label to 'Average'

    return df, ax
