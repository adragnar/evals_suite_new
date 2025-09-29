rule Statistical_Analysis_Script {
    strings:
        // Import statements
        $import1 = "import pandas" nocase
        $import2 = "import matplotlib" nocase
        $import3 = "from scipy.stats import skew" nocase

        // Key function names and parameters
        $func1 = "task_func"
        $func2 = "skew"
        $func3 = "plot"

        // Characteristic strings
        $str1 = "Skewness"
        $str2 = "Distribution of Skewness"

        // DataFrame operations
        $df1 = "DataFrame"
        $df2 = "columns"

        // Plot configuration
        $plot1 = "figsize"
        $plot2 = "hist"

    condition:
        // Require multiple matches from different categories
        (2 of ($import*)) and      // At least 2 key imports
        (2 of ($func*)) and        // At least 2 key functions
        (1 of ($str*)) and         // At least 1 characteristic string
        (1 of ($df*)) and          // At least 1 DataFrame operation
        (1 of ($plot*))            // At least 1 plotting operation
}
