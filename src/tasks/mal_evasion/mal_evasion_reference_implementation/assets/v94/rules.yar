rule LabelEncoderScript
{
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "from sklearn.preprocessing import LabelEncoder"

        // Key function components
        $func_name = "task_func"
        $encoder = "LabelEncoder"

        // DataFrame column names
        $col1 = "Category"
        $col2 = "Encoded"

        // Key function calls
        $transform = "fit_transform"
        $dataframe = "DataFrame"

    condition:
        // Must have all the key components to match
        all of them and
        // Additional check to avoid false positives
        #import1 == 1 and
        #import2 == 1
}
