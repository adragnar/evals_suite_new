rule DataAnalysisPython
{
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "import regex as re"
        $import3 = "import seaborn as sns"
        $import4 = "import matplotlib.pyplot as plt"

        // Column names constant
        $cols = "COLUMN_NAMES = [\"Name\", \"Email\", \"Age\", \"Country\"]"

        // Function definition
        $func = "def task_func"

        // Key regex pattern
        $pattern = "Name: (.*?), Email: (.*?), Age: (.*?), Country: (.*?)($|\\n)"

        // DataFrame operations
        $df1 = "pd.DataFrame"
        $df2 = "df[\"Age\"] ="

        // Visualization
        $viz1 = "sns.histplot"
        $viz2 = "plt.show"

    condition:
        // Require enough specific matches to avoid false positives
        // Must have at least 3 imports, the column names, function def,
        // and some DataFrame operations
        (3 of ($import*)) and
        $cols and
        $func and
        $pattern and
        (1 of ($df*)) and
        (1 of ($viz*))
}
