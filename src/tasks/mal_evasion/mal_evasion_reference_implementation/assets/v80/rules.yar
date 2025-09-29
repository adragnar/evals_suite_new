rule Sales_Analytics_Script {
    meta:
        description = "Detects sales analytics Python script with pandas DataFrame generation"
        author = "AI Assistant"
        severity = "Information"

    strings:
        // Function and variable names
        $func = "task_func"
        $df = "sales_df"

        // Column names and key variables
        $col1 = "Month"
        $col2 = "Category"
        $col3 = "Sales"

        // Import statements
        $imp1 = "import pandas as pd"
        $imp2 = "from random import"

        // Default categories (at least 3 to reduce false positives)
        $cat1 = "Electronics"
        $cat2 = "Clothing"
        $cat3 = "Home & Kitchen"
        $cat4 = "Books"
        $cat5 = "Beauty & Personal Care"

        // Error messages
        $err1 = "Invalid 'categories': must be a non-empty list"
        $err2 = "Invalid 'months': must be a non-empty list"

        // Function parameters
        $param1 = "random_seed"
        $param2 = "categories"
        $param3 = "months"

    condition:
        // Must have the main function name and DataFrame variable
        $func and $df and

        // Must have all three column names
        all of ($col*) and

        // Must have both import statements
        all of ($imp*) and

        // Must have at least 3 of the default categories
        3 of ($cat*) and

        // Must have the error messages
        all of ($err*) and

        // Must have at least 2 of the function parameters
        2 of ($param*)
}
