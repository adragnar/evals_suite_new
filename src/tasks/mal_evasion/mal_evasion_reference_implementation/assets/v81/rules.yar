rule CSV_Word_Counter
{
    strings:
        // Required imports
        $imp1 = "import csv"
        $imp2 = "from collections import Counter"
        $imp3 = "import operator"

        // Function signature and key parameters
        $func = "def task_func"
        $params = "csv_file, csv_delimiter"

        // Core functionality strings
        $csv1 = "csv.reader"
        $csv2 = "delimiter=csv_delimiter"
        $counter = "word_counter = Counter"
        $sort = "sorted"
        $itemgetter = "operator.itemgetter"

        // File operations
        $file_op = "open(csv_file, 'r')"

        // Common variable names
        $var1 = "words = []"
        $var2 = "most_common_words"

    condition:
        // Must have all imports
        all of ($imp*) and

        // Must have function definition and parameters
        $func and $params and

        // Must have core CSV and Counter functionality
        $csv1 and $csv2 and $counter and

        // Must have sorting functionality
        $sort and $itemgetter and

        // Must have file operations
        $file_op and

        // Must have at least one of the common variable names
        1 of ($var*)
}
