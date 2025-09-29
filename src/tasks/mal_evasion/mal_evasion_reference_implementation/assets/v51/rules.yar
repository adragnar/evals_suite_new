rule Data_Extraction_Script {
    strings:
        // Import statements
        $import1 = "import pandas" nocase
        $import2 = "import regex" nocase

        // Common DataFrame operations
        $df1 = "DataFrame" nocase
        $df2 = "astype" nocase
        $df3 = "columns" nocase

        // Regex pattern components
        $pattern1 = "Score: "
        $pattern2 = "Category: "
        $pattern3 = "pattern"
        $pattern4 = "findall"

        // Function components
        $func1 = "task_func"
        $func2 = "text"
        $func3 = "matches"

        // Type conversion
        $type1 = "astype(int)"
        $type2 = "int)"

        // DataFrame column names
        $col1 = "Score"
        $col2 = "Category"

    condition:
        // Must have both imports
        ($import1 and $import2) and

        // Must have DataFrame operations
        (2 of ($df*)) and

        // Must have regex pattern matching
        (2 of ($pattern*)) and

        // Must have at least some function components
        (1 of ($func*)) and

        // Must have type conversion
        (1 of ($type*)) and

        // Must have column names
        ($col1 and $col2)
}
