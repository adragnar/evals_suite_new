rule Python_Sales_Report_Generator
{
    strings:
        // Import statements
        $import1 = "import numpy as np"
        $import2 = "import pandas as pd"

        // Function definition and key parameters
        $func_def = "def task_func"
        $param1 = "products"
        $param2 = "n_samples"
        $param3 = "sales_lower"
        $param4 = "profit_margin"

        // Distinctive docstring elements
        $doc1 = "Generate a sales report with randomly simulated sales"
        $doc2 = "Parameters:"
        $doc3 = "Returns:"
        $doc4 = "pd.DataFrame"

        // Key operations
        $op1 = "np.random.seed"
        $op2 = "groupby"
        $op3 = "sort_values"
        $op4 = "np.random.randint"

        // Error handling
        $err1 = "ValueError"
        $err2 = "TypeError"
        $err3 = "products must be a list of strings"

    condition:
        // Must have both imports
        all of ($import*) and

        // Must have function definition and at least 3 of the parameters
        $func_def and 3 of ($param*) and

        // Must have at least 2 docstring elements
        2 of ($doc*) and

        // Must have at least 2 key operations
        2 of ($op*) and

        // Must have at least 2 error handling elements
        2 of ($err*)
}
