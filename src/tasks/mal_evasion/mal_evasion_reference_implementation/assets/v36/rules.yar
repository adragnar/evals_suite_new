rule Data_Analysis_Program
{
    strings:
        // Import statements
        $import1 = "import pandas"
        $import2 = "from sklearn.preprocessing import StandardScaler"
        $import3 = "import matplotlib.pyplot"

        // Key function and variable names
        $func1 = "StandardScaler"
        $func2 = "DataFrame"
        $func3 = "plot"
        $func4 = "hist"

        // Distinctive strings
        $str1 = "Distribution of Means"
        $str2 = "Feature"
        $str3 = "Mean"

        // Data processing indicators
        $data1 = "standardized_data"
        $data2 = "data_matrix"
        $data3 = "axis=1"
        $data4 = "fit_transform"

    condition:
        // Must have key imports
        2 of ($import*) and

        // Must have some key function names
        2 of ($func*) and

        // Must have some distinctive strings
        2 of ($str*) and

        // Must have data processing indicators
        2 of ($data*)
}
