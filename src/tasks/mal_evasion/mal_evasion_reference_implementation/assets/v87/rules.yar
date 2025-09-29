rule Python_Temperature_Plotting_Program
{
    strings:
        // Key imports
        $import1 = "import matplotlib.pyplot"
        $import2 = "import pandas"

        // Function definition and key parameters
        $func_def = "def task_func"
        $param = "temperatures"

        // Distinctive plot strings
        $label1 = "Date"
        $label2 = "Temperature"
        $title = "Daily Temperatures in New York"

        // Font configuration
        $font1 = "Arial"
        $font2 = "sans-serif"

        // Docstring content
        $doc1 = "Calculate and plot the daytime temperatures"
        $doc2 = "Parameters:"
        $doc3 = "Returns:"

        // Error handling
        $error1 = "ValueError"
        $error2 = "An error occurred:"

    condition:
        // Must have both imports
        ($import1 and $import2) and

        // Must have function definition and parameter
        ($func_def and $param) and

        // Must have at least 2 of the plot labels/title
        2 of ($label1, $label2, $title) and

        // Must have font configuration
        ($font1 and $font2) and

        // Must have at least 2 docstring elements
        2 of ($doc1, $doc2, $doc3) and

        // Must have error handling
        ($error1 or $error2)
}
