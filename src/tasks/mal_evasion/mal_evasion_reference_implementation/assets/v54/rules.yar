rule Python_CSV_JSON_Converter
{
    strings:
        // Import statements
        $import1 = "import json" nocase
        $import2 = "import pandas" nocase

        // Function definition
        $func = "def task_func" nocase

        // Key parameters and variables
        $param1 = "result" nocase
        $param2 = "csv_file_path" nocase
        $param3 = "json_file_path" nocase

        // File operations
        $file_op1 = ".to_csv" nocase
        $file_op2 = "json.dump" nocase

        // File extensions
        $ext1 = ".csv"
        $ext2 = ".json"

        // DataFrame operations
        $df = "pd.DataFrame" nocase

    condition:
        // Must have imports
        ($import1 and $import2) and

        // Must have function definition
        $func and

        // Must have at least 2 parameters
        2 of ($param*) and

        // Must have both file operations
        all of ($file_op*) and

        // Must have both extensions
        all of ($ext*) and

        // Must have DataFrame operation
        $df
}
