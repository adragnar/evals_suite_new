rule Python_Data_Visualization_Correlation_Heatmap {
    meta:
        description = "Detects Python code that creates correlation heatmaps using pandas/seaborn"
        author = "AI Assistant"

    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "import matplotlib.pyplot as plt"
        $import3 = "import seaborn as sns"

        // Function definition and parameters
        $func_def = "def task_func"
        $param1 = "csv_file_path"
        $param2 = "title"

        // Key function calls
        $read_csv = "pd.read_csv"
        $corr = ".corr()"
        $heatmap = "sns.heatmap"

        // Characteristic strings
        $annot = "annot=True"
        $cmap = "cmap='coolwarm'"
        $figsize = "figsize="
        $round = ".round"

        // Docstring elements
        $docstring1 = "Create a heatmap"
        $docstring2 = "Parameters:"
        $docstring3 = "Returns:"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have function definition and key parameters
        $func_def and all of ($param*) and

        // Must have key visualization function calls
        all of ($read_csv, $corr, $heatmap) and

        // Must have at least 2 characteristic heatmap configuration strings
        2 of ($annot, $cmap, $figsize, $round) and

        // Must have at least 2 docstring elements
        2 of ($docstring*)
}
