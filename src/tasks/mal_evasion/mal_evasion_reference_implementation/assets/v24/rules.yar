rule Python_List_Combination_Task
{
    strings:
        // Import statements
        $import1 = "import collections"
        $import2 = "from itertools import zip_longest"
        $import3 = "from random import choices"

        // Key function names and method calls
        $func1 = "def task_func"
        $func2 = "zip_longest"
        $func3 = "choices"
        $func4 = "Counter"

        // Characteristic variable names
        $var1 = "combined"
        $var2 = "sample"
        $var3 = "freq"

    condition:
        // Require at least 2 imports and 2 key functions to match
        // This helps avoid false positives while still being flexible enough
        2 of ($import*) and
        2 of ($func*) and
        1 of ($var*) and
        // Total number of identified strings should be at least 5
        // This ensures enough characteristic elements are present
        5 of them
}
