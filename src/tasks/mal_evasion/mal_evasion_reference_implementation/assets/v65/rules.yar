rule Data_Analysis_Script {
    meta:
        description = "Detects data analysis scripts using pandas/seaborn for statistical operations"
        author = "AI Assistant"
        severity = "info"

    strings:
        // Import statements
        $import1 = "import pandas" nocase
        $import2 = "import seaborn" nocase
        $import3 = "import numpy" nocase

        // Function components
        $func = "def task_func"
        $param = "csv_file"

        // Statistical operations
        $stat1 = "'mean'"
        $stat2 = "'std'"
        $stat3 = "'sum'"

        // Dataframe operations
        $df1 = "pd.read_csv"
        $df2 = "df['list']"

        // Plotting
        $plot = "sns.histplot"

    condition:
        // Must have at least 2 of the imports
        2 of ($import*) and

        // Must have the function definition and parameter
        ($func and $param) and

        // Must have at least 2 statistical operations
        2 of ($stat*) and

        // Must have at least 1 dataframe operation
        1 of ($df*) and

        // Must have plotting
        $plot
}
