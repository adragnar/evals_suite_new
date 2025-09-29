rule Python_DataFrame_Visualization {
    strings:
        // Import statements
        $imp1 = "import ast" ascii
        $imp2 = "import pandas" ascii
        $imp3 = "import seaborn" ascii

        // Function definition and docstring
        $func = "def task_func" ascii
        $param = "csv_file" ascii

        // Key operations
        $op1 = "read_csv" ascii
        $op2 = "literal_eval" ascii
        $op3 = "pairplot" ascii

        // Column names
        $col1 = "dict_column" ascii
        $col2 = "hue_column" ascii

        // Return statement pattern
        $ret = "return df, ax" ascii

    condition:
        // Require multiple matches to confirm it's this specific program
        all of ($imp*) and
        $func and
        $param and
        all of ($op*) and
        all of ($col*) and
        $ret and
        // Additional constraint to avoid false positives
        #col1 >= 2  // dict_column appears multiple times
}
