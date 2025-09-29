rule DataFrame_Visualization_Script {
    meta:
        description = "Detects pandas/matplotlib data visualization script with specific structure"

    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "import matplotlib.pyplot as plt"

        // Key variables and constants
        $columns = "COLUMNS = ['col1', 'col2', 'col3']"
        $func_def = "def task_func"

        // DataFrame operations
        $df_op1 = "DataFrame("
        $df_op2 = "groupby"
        $df_op3 = "nunique"
        $df_op4 = "reset_index"

        // Plotting operations
        $plot1 = "plt.subplots"
        $plot2 = "ax.plot"
        $plot3 = "ax.set_xlabel"
        $plot4 = "ax.set_ylabel"

        // Return statement signature
        $ret = "return analyzed_df, ax"

        // Doc strings
        $doc1 = "Parameters:"
        $doc2 = "Returns:"
        $doc3 = "Requirements:"

    condition:
        // Must have both imports
        ($import1 and $import2) and

        // Must have the columns definition and function definition
        ($columns and $func_def) and

        // Must have at least 3 of the 4 DataFrame operations
        3 of ($df_op*) and

        // Must have at least 3 of the 4 plotting operations
        3 of ($plot*) and

        // Must have the return statement
        $ret and

        // Must have at least 2 of the 3 documentation strings
        2 of ($doc*)
}
