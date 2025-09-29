rule Python_DataViz_Script {
    meta:
        description = "Detects Python data visualization script with specific pandas/matplotlib usage"
        author = "AI Assistant"

    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "import matplotlib.pyplot as plt"
        $import3 = "from itertools import cycle"

        // Function definition and docstring elements
        $func_def = "def task_func"
        $param1 = "df"
        $param2 = "groups="

        // Key visualization strings
        $plot_title = "Scatterplot of Values for Each Group Over Time"
        $xlabel = "Date (ordinal)"
        $ylabel = "Value"

        // Key DataFrame operations
        $df_check = "isinstance(df, pd.DataFrame)"
        $columns = "'group', 'date', 'value'"

        // Plot configuration
        $scatter = ".scatter("
        $set_title = ".set_title("

        // Error handling
        $error = "raise ValueError"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have function definition and parameters
        $func_def and all of ($param*) and

        // Must have plot labels
        all of ($plot_title, $xlabel, $ylabel) and

        // Must have DataFrame operations
        $df_check and $columns and

        // Must have plot configuration
        all of ($scatter, $set_title) and

        // Must have error handling
        $error
}
