import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Constants
PLOT_TITLE = "Square root plot"
X_LABEL = "x"
Y_LABEL = "sqrt(x)"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def task_func(result):
    """
    Plots the square root function for values associated with the key 'from_user' from the input list of dictionaries. Annotates the graph with the current date and time.
    - Round each square root value to 2 decimals.

    Parameters:
    result (list): A list of dictionaries containing numeric values with the key 'from_user'.

    Returns:
    - numpy.ndarray: list of square values associated with the key 'from_user' from the input list of dictionaries.
    - matplotlib.axes.Axes: plot of square root values.

    Requirements:
    - numpy
    - matplotlib.pyplot
    - datetime

    Constants:
    - PLOT_TITLE: Title of the plot (default is 'Square root plot').
    - X_LABEL: Label for the x-axis (default is 'x').
    - Y_LABEL: Label for the y-axis (default is 'sqrt(x)').
    - TIME_FORMAT: Format for displaying the current date and time (default is '%Y-%m-%d %H:%M:%S').

    Example:
    >>> result = [{"hi": 7, "bye": 4, "from_user": 16}, {"some_key": 2, "another_key": 4, "from_user": 9}]
    >>> square_roots, ax = task_func(result)
    >>> print(square_roots)
    [4. 3.]
    """

    # Extract the 'from_user' values
    from_user_values = [d["from_user"] for d in result if "from_user" in d]

    # Calculate the square roots
    square_roots = np.round(np.sqrt(from_user_values), 2)

    # Plot the square root function
    plt.figure()
    plt.plot(from_user_values, square_roots)
    plt.title(PLOT_TITLE)
    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)

    # Annotate the plot with the current date and time
    now = datetime.now()
    now_str = now.strftime(TIME_FORMAT)
    plt.annotate(now_str, (0.05, 0.95), xycoords="axes fraction")
    ax = plt.gca()
    return square_roots, ax
