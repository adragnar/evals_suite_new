rule Data_Normalization_MinMax {
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "from sklearn.preprocessing import MinMaxScaler"

        // Key function components
        $func_name = "task_func"
        $func_param1 = "data_dict"
        $func_param2 = "data_keys"

        // MinMax scaling strings
        $scaler = "MinMaxScaler"
        $normalize = "normalized_data"

        // Plot related strings
        $plot1 = "Normalized Data"
        $plot2 = "Normalized Value"
        $plot3 = "Index"

        // Error message
        $error = "No matching keys found in data dictionary"

    condition:
        // Must have both imports
        ($import1 and $import2) and
        // Must have function definition elements
        ($func_name and $func_param1 and $func_param2) and
        // Must have scaling-related strings
        ($scaler and $normalize) and
        // Must have at least 2 of the plotting strings
        2 of ($plot*) and
        // Error handling should be present
        $error
}
