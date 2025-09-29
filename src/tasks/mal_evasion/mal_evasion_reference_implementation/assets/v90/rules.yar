rule DataNormalizationFunction
{
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "from sklearn.preprocessing import MinMaxScaler"

        // Key function components
        $func_def = "def task_func"
        $scaler = "MinMaxScaler()"

        // DataFrame operations
        $df1 = "DataFrame"
        $df2 = "to_string"

        // Error handling
        $error = "ValueError"

        // Plot related
        $plot1 = "plot(kind='line')"
        $plot2 = "set_title"
        $plot3 = "set_ylabel"
        $plot4 = "set_xlabel"

        // Normalization related
        $norm1 = "normalized_data"
        $norm2 = "fit_transform"

    condition:
        // Must have both imports
        all of ($import*) and

        // Must have function definition and scaler
        $func_def and $scaler and

        // Must have DataFrame operations
        all of ($df*) and

        // Must have error handling
        $error and

        // Must have at least 3 plotting operations
        3 of ($plot*) and

        // Must have normalization operations
        all of ($norm*)
}
