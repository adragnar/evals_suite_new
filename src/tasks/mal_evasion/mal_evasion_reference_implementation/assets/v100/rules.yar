rule Statistical_Data_Analysis_Script
{
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "import seaborn as sns"
        $import3 = "from scipy import stats"

        // Function name and core components
        $func = "def task_func"
        $columns = "COLUMN_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']"

        // Statistical operations
        $stat1 = "stats.normaltest"
        $stat2 = "sns.kdeplot"
        $stat3 = "df.mean"

        // Error messages and comments
        $error = "Data must contain exactly eight columns"
        $docstring = "Processes a given dataset to compute the average of each row"

        // DataFrame operations
        $df1 = "pd.DataFrame"
        $df2 = "axis=1"

        // Key variable names
        $var1 = "Average"
        $var2 = "linewidth"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have function definition and column names
        $func and $columns and

        // Must have at least 2 statistical operations
        2 of ($stat*) and

        // Must have error handling and documentation
        $error and $docstring and

        // Must have DataFrame operations
        all of ($df*) and

        // Must have at least one key variable name
        1 of ($var*)
}
