rule Statistical_Plotting_Function
{
    strings:
        // Import statements
        $import1 = "from scipy.stats import linregress"
        $import2 = "import matplotlib.pyplot"

        // Function definition and parameters
        $func = "def task_func"
        $param1 = "data"
        $param2 = "column1"
        $param3 = "column2"

        // Key operations and variables
        $stats1 = "linregress"
        $stats2 = "slope"
        $stats3 = "intercept"
        $stats4 = "r_value"
        $stats5 = "p_value"

        // Plotting related
        $plot1 = "plt.subplots"
        $plot2 = "ax.plot"
        $plot3 = "fitted line"
        $plot4 = "original data"

        // Error handling
        $error = "Specified columns must exist in the DataFrame"

    condition:
        // Must have both imports
        all of ($import*) and

        // Must have function definition
        $func and

        // Must have at least 2 of the parameters
        2 of ($param*) and

        // Must have at least 3 statistical keywords
        3 of ($stats*) and

        // Must have at least 3 plotting keywords
        3 of ($plot*) and

        // Error handling is present
        $error
}
