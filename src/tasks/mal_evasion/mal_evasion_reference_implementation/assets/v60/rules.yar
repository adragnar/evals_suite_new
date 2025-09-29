rule Python_DataAnalysis_TaskFunc {
    strings:
        // Imports and constants
        $import1 = "import pandas as pd"
        $import2 = "import seaborn as sns"
        $columns = "COLUMNS = ['col1', 'col2', 'col3']"

        // Function definition and key variables
        $func_def = "def task_func"
        $df_ops1 = "df = pd.DataFrame"
        $df_ops2 = "analyzed_df ="
        $df_ops3 = ".groupby"
        $df_ops4 = ".reset_index()"

        // Distinctive docstring fragments
        $doc1 = "You are given a list of elements"
        $doc2 = "distribution of chart"
        $doc3 = "Parameters:"
        $doc4 = "Returns:"

        // Seaborn plot
        $plot = "sns.distplot"

    condition:
        // Must have both imports
        all of ($import*) and

        // Must have COLUMNS constant
        $columns and

        // Must have function definition and key DataFrame operations
        $func_def and
        all of ($df_ops*) and

        // Must have at least 3 of the docstring elements
        3 of ($doc*) and

        // Must have seaborn plot
        $plot and

        // Additional constraint: strings should appear in reasonable proximity
        @import1 < @import2 + 100 and  // imports should be close together
        @columns < @func_def + 200      // COLUMNS constant should be before function def
}
