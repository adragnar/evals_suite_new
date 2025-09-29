rule DataProcessingVisualization
{
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "import seaborn as sns"

        // Function signature and docstring elements
        $func_def = "def task_func"
        $param1 = "data="
        $param2 = "emp_prefix="

        // DataFrame operations
        $df_op1 = "pd.read_csv"
        $df_op2 = "df["
        $df_op3 = ".str.startswith"

        // Column names and visualization
        $col1 = "'Employee ID'"
        $col2 = "'Age'"
        $viz = "sns.histplot"

        // Return statement components
        $ret = "return df, ax"

    condition:
        // Must have both imports
        ($import1 and $import2) and

        // Must have function definition and key parameters
        $func_def and ($param1 or $param2) and

        // Must have DataFrame operations
        2 of ($df_op*) and

        // Must have visualization elements
        $viz and

        // Must have at least one of the column names
        1 of ($col*) and

        // Must have return statement
        $ret
}
