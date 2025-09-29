from scipy.stats import linregress
import matplotlib.pyplot as plt


def task_func(data, column1, column2):
    """
    Perform a linear regression on two columns of a dataset and record the result.
    Additionally, generates a plot representing the original data and the fitted line.

    Parameters:
    data (DataFrame): The dataset.
    column1 (str): The name of the first column.
    column2 (str): The name of the second column.

    Returns:
    tuple: The slope, intercept, r-value, p-value, and standard error of the regression.
    Axes: The matplotlib Axes object containing the plot.

    Raises:
    ValueError: If the specified columns do not exist in the DataFrame.

    Requirements:
    - scipy.stats
    - matplotlib.pyplot

    Example:
    >>> data = pd.DataFrame([[14, 25], [1, 22], [7, 8]], columns=['Column1', 'Column2'])
    >>> result, ax = task_func(data, 'Column1', 'Column2')
    """

    if column1 not in data.columns or column2 not in data.columns:
        raise ValueError("Specified columns must exist in the DataFrame")

    x = data[column1].values
    y = data[column2].values

    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    fig, ax = plt.subplots()
    ax.plot(x, y, "o", label="original data")
    ax.plot(x, intercept + slope * x, "r", label="fitted line")
    ax.legend()

    return (slope, intercept, r_value, p_value, std_err), ax
