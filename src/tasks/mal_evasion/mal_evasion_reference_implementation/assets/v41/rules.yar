rule Python_PCA_DataAnalysis
{
    strings:
        // Import statements
        $import1 = "import pandas" nocase
        $import2 = "import numpy" nocase
        $import3 = "from sklearn.decomposition import PCA" nocase
        $import4 = "import seaborn" nocase
        $import5 = "import matplotlib" nocase

        // Key function names and patterns
        $func1 = "def task_func" nocase
        $func2 = "PCA(n_components=2)" nocase
        $func3 = "sns.scatterplot" nocase

        // Specific data patterns
        $data1 = "Component 1"
        $data2 = "Component 2"

        // Key operations
        $op1 = "principalComponents" nocase
        $op2 = "fit_transform" nocase
        $op3 = "select_dtypes" nocase
        $op4 = "fillna" nocase

    condition:
        // Require multiple matches from different categories
        (3 of ($import*)) and      // At least 3 of the imports
        (2 of ($func*)) and        // At least 2 of the functions
        (all of ($data*)) and      // Both component strings
        (2 of ($op*))              // At least 2 operations
}
