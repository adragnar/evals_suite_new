rule Python_Data_Processing_Task {
    meta:
        description = "Detects Python data processing script with normalization and visualization"
        author = "Assistant"
        severity = "Info"

    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "from sklearn.preprocessing import MinMaxScaler"
        $import3 = "import matplotlib.pyplot"

        // Function definition and key components
        $func_def = "def task_func"
        $docstring = "Normalizes a given dataset using MinMax scaling"

        // Column names and key variables
        $cols = "COLUMN_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']"
        $avg = "'Average'"

        // Key operations
        $normalize = "normalized_data = scaler.fit_transform"
        $df_create = "pd.DataFrame"
        $plot = "plot(ax=ax)"

        // Example usage in docstring
        $example = ">>> data = np.array"

    condition:
        // Must have the core imports
        ($import1 and $import2 and $import3) and
        // Must have function definition and docstring
        ($func_def and $docstring) and
        // Must have column names and DataFrame creation
        ($cols and $df_create) and
        // Must have at least one key operation
        ($normalize or $plot) and
        // Should have the Average column
        $avg and
        // Should have example usage
        $example
}
