rule Email_Data_Analysis_Script {
    meta:
        description = "Detects Python script for email data analysis with SQLite and pandas"
        author = "AI Assistant"

    strings:
        // Import statements
        $import1 = "import pandas" nocase
        $import2 = "import sqlite3" nocase
        $import3 = "import numpy" nocase
        $import4 = "import matplotlib" nocase
        $import5 = "import ast" nocase

        // Function definition and key features
        $func = "def task_func" nocase

        // Key operations and variables
        $sql1 = "SELECT * FROM EmailData" nocase
        $df1 = ".read_sql_query"
        $df2 = "df['list']"
        $df3 = ".literal_eval"

        // Statistical operations
        $stat1 = "'sum'"
        $stat2 = "'mean'"
        $stat3 = "'var'"
        $stat4 = ".apply(np"

        // Plotting
        $plot1 = ".plot(kind='bar')"
        $plot2 = "plt.show()"

    condition:
        // Must have most imports
        3 of ($import*) and

        // Must have function definition
        $func and

        // Must have DataFrame and SQL operations
        2 of ($df*) and
        $sql1 and

        // Must have statistical operations
        2 of ($stat*) and

        // Must have plotting
        1 of ($plot*)
}
