rule DataAnalysisEmailProcessor
{
    strings:
        // Library imports
        $import1 = "import pandas"
        $import2 = "import json"
        $import3 = "import numpy"

        // Column names and data structures
        $col1 = "email"
        $col2 = "list"
        $col3 = "sum"
        $col4 = "mean"

        // File operations
        $file_op1 = "open("
        $file_op2 = "'r'"
        $file_op3 = "json.load"

        // Data analysis operations
        $op1 = "DataFrame"
        $op2 = "apply"
        $op3 = "np.sum"
        $op4 = "np.mean"

        // Plotting
        $plot1 = "plot"
        $plot2 = "bar"
        $plot3 = "ax"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have all column names
        all of ($col*) and

        // Must have file operations
        2 of ($file_op*) and

        // Must have data analysis operations
        2 of ($op*) and

        // Must have plotting functionality
        2 of ($plot*)
}
