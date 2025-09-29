rule CSV_Sales_Processor
{
    strings:
        // Import patterns
        $import1 = "import csv"
        $import2 = "import collections"
        $import3 = "import operator"

        // Function and argument patterns
        $func = "def task_func"
        $arg = "csv_file_path"

        // File operation patterns
        $file_op1 = "open("
        $file_op2 = "'r'"

        // CSV processing patterns
        $csv1 = "csv.reader"
        $csv2 = "next(reader)"

        // Data structure patterns
        $data1 = "defaultdict"
        $data2 = "sales_data"

        // Column identifiers
        $col1 = "product"
        $col2 = "quantity"

        // Processing patterns
        $proc1 = "top_selling_product"
        $proc2 = "max("
        $proc3 = "itemgetter"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have function definition and argument
        $func and $arg and

        // Must have file operations
        all of ($file_op*) and

        // Must have CSV processing
        all of ($csv*) and

        // Must have data structure elements
        all of ($data*) and

        // Must have column identifiers
        all of ($col*) and

        // Must have processing elements
        2 of ($proc*)
}
