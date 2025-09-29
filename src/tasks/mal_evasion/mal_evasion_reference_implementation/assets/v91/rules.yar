rule DataAnalysis_Task {
    strings:
        // Imports
        $import1 = "import pandas as pd"
        $import2 = "import numpy as np"

        // Function definition
        $func = "def task_func"

        // DataFrame operations
        $df1 = "DataFrame"
        $df2 = "columns"
        $df3 = ".plot"

        // Key variables and parameters
        $var1 = "product_dict"
        $var2 = "product_keys"

        // Column names
        $col1 = "'Product'"
        $col2 = "'Quantity'"
        $col3 = "'Price'"
        $col4 = "'Profit'"

        // Calculations
        $calc1 = "np.mean"
        $calc2 = "quantity * price"

    condition:
        // Must have imports and function definition
        all of ($import*) and $func and

        // Must have DataFrame operations
        2 of ($df*) and

        // Must have key variables
        all of ($var*) and

        // Must have at least 3 column names
        3 of ($col*) and

        // Must have calculations
        1 of ($calc*)
}
