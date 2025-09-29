rule DataVisualizationScript
{
    strings:
        // Import statements
        $imp1 = "import pandas as pd"
        $imp2 = "import seaborn as sns"
        $imp3 = "import matplotlib.pyplot as plt"

        // Column names
        $cols = "COLUMNS = ['col1', 'col2', 'col3']"

        // Key pandas operations
        $op1 = "groupby"
        $op2 = "pivot"
        $op3 = "DataFrame"

        // Visualization elements
        $viz1 = "sns.heatmap"
        $viz2 = "plt.show"

        // Function definition
        $func = "def task_func"

    condition:
        // Must have all imports
        all of ($imp*) and

        // Must have column definitions
        $cols and

        // Must have at least 2 pandas operations
        2 of ($op*) and

        // Must have visualization code
        all of ($viz*) and

        // Must have the main function
        $func
}
