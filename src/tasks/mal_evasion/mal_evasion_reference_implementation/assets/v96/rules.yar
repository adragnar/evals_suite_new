rule Python_DataAnalysis_Script
{
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "import matplotlib.pyplot"

        // Function definition and key strings
        $func_def = "def task_func"
        $docstring = "Computes the average of each row"

        // Column names constant
        $columns = "COLUMN_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']"

        // Key pandas/matplotlib operations
        $df1 = "DataFrame"
        $df2 = "df.mean"
        $plot = "df['Average'].plot"

        // Required package comments
        $req1 = "- pandas"
        $req2 = "- matplotlib"

        // Example usage in docstring
        $example = ">>> import numpy"

    condition:
        // Must contain both imports
        ($import1 and $import2) and

        // Must contain function definition and docstring
        ($func_def and $docstring) and

        // Must contain column names definition
        $columns and

        // Must contain at least 2 DataFrame/plotting operations
        2 of ($df1, $df2, $plot) and

        // Must contain requirements and example
        ($req1 and $req2 and $example)
}
