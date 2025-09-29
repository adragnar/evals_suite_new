rule DataVisualizationProgram
{
    strings:
        // Import statements
        $import1 = "import matplotlib.pyplot" nocase
        $import2 = "import pandas" nocase
        $import3 = "from datetime import datetime" nocase

        // Function definition and key components
        $func = "def task_func" nocase

        // Plot labels and titles
        $label1 = "Random Time Series Data"
        $label2 = "Value over Time"
        $label3 = "Date"
        $label4 = "Value"

        // Font setting
        $font = "plt.rc('font', family='Arial')" nocase

        // Error handling
        $error = "Error generating the plot:"

        // Key function calls
        $pandas1 = "pd.date_range"
        $plot1 = "plt.subplots"

    condition:
        // Must have either all imports or function name plus key strings
        (all of ($import*)) or
        ($func and 3 of ($label*)) and
        // Must have some plotting functionality
        ($plot1 or $pandas1) and
        // Should have at least 6 of the defined strings total
        6 of them
}
