rule Python_DataAnalysis_ProfitReport
{
    strings:
        // Imports
        $import1 = "import pandas as pd"
        $import2 = "import numpy as np"

        // Function definition
        $func = "def task_func"

        // Key column names and variables
        $col1 = "'Product'"
        $col2 = "'Quantity'"
        $col3 = "'Price'"
        $col4 = "'Profit'"
        $col5 = "'Average Price'"
        $col6 = "'Average Profit'"

        // Plotting related
        $plot1 = "plot(x='Product', y='Profit', kind='bar'"
        $plot2 = "set_ylabel"

        // DataFrame operations
        $df1 = "DataFrame"
        $df2 = "columns"

        // Calculation related
        $calc1 = "np.mean"
        $calc2 = "quantity * price"

    condition:
        // Must have both imports
        all of ($import*) and

        // Must have the main function definition
        $func and

        // Must have at least 4 of the column names
        4 of ($col*) and

        // Must have either plotting or DataFrame operations
        (1 of ($plot*) or all of ($df*)) and

        // Must have at least one calculation
        1 of ($calc*)
}
