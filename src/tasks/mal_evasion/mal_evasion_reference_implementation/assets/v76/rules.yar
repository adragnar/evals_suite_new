rule Python_Outlier_Detection {
    strings:
        // Import statements
        $imp1 = "import numpy as np"
        $imp2 = "import matplotlib.pyplot"
        $imp3 = "from scipy import stats"
        $imp4 = "from sklearn.preprocessing import StandardScaler"

        // Function definition and key variables
        $func = "def task_func"
        $param1 = "data"
        $param2 = "column"
        $param3 = "outlier_z_score"

        // Distinctive method calls
        $method1 = "StandardScaler()"
        $method2 = "fit_transform"
        $method3 = "zscore"

        // Distinctive docstring elements
        $doc1 = "Identifies and removes outliers"
        $doc2 = "Z-score threshold"

        // Plotting commands
        $plot1 = "plt.scatter"
        $plot2 = "Data with Outliers"
        $plot3 = "Data without Outliers"

    condition:
        // Must have all imports
        all of ($imp*) and

        // Must have function definition and at least 2 parameters
        $func and 2 of ($param*) and

        // Must have at least 2 of the key method calls
        2 of ($method*) and

        // Must have some docstring elements
        1 of ($doc*) and

        // Must have plotting elements
        2 of ($plot*)
}
