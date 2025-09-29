rule Python_SquareRoot_Plotting_Script
{
    strings:
        // Import statements
        $import1 = "import numpy as np"
        $import2 = "import matplotlib.pyplot as plt"
        $import3 = "from datetime import datetime"

        // Constants
        $const1 = "PLOT_TITLE = 'Square root plot'"
        $const2 = "TIME_FORMAT = '%Y-%m-%d %H:%M:%S'"

        // Function signature and key operations
        $func1 = "def task_func"
        $func2 = "square_roots = np.round(np.sqrt"

        // Plot operations
        $plot1 = "plt.figure()"
        $plot2 = "plt.plot"
        $plot3 = "plt.title"
        $plot4 = "plt.annotate"

        // Key variables
        $var1 = "from_user_values"
        $var2 = "square_roots"

    condition:
        // Must have all imports
        all of ($import*) and
        // Must have at least one constant definition
        1 of ($const*) and
        // Must have function definition and square root calculation
        all of ($func*) and
        // Must have at least 2 plotting operations
        2 of ($plot*) and
        // Must have at least one of the key variables
        1 of ($var*)
}
