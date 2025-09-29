import pandas as pd
import os
import numpy as np
import ast


def task_func(directory):
    """
    Traverse a directory for CSV files a get the file with the longest filename. From that CSV file, load e-mail data, convert it into a Pandas DataFrame, calculate the sum, mean and median of the list associated with each e-mail, and then draw a histogram of the median.
    - The column names of each CSV files are 'email' and 'list'.
    - The column 'list' contains a string representation of a list. It should be converted before usage.
    - If there is not csv file in the directory, return an empty dataframe with the columns expected.
    - If there is not csv file in the directory, return None instead of an empty plot.

    Parameters:
    - directory (str): The path to the directory.

    Returns:
    - pandas.DataFrame : DataFrame containing the data from the CSV file with the longest filename augmented with the columns 'sum', 'mean' and 'median'.
    - matplotlib.axes._axes.Axes : Histogram of the median. None if there is no data to plot.

    Requirements:
    - pandas
    - os
    - numpy
    - ast

    Example:
    >>> task_func('data_directory')
    """

    name = None
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            if name is None:
                name = filename
            else:
                name = filename if len(filename) > len(name) else name
    if name is None:
        return pd.DataFrame(
            {}, columns=["email", "list"] + ["sum", "mean", "median"]
        ), None

    df = pd.read_csv(os.path.join(directory, name))
    df["list"] = df["list"].map(ast.literal_eval)
    df["sum"] = df["list"].apply(sum)
    df["mean"] = df["list"].apply(np.mean)
    df["median"] = df["list"].apply(np.median)

    return df, df["median"].hist()
