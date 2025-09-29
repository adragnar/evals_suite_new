rule Text_Analysis_Tool
{
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "import regex as re"

        // Stopwords constant
        $stopwords = "STOPWORDS = [" ascii
        $sw1 = "\"a\"" ascii
        $sw2 = "\"the\"" ascii
        $sw3 = "\"in\"" ascii

        // Function components
        $func_def = "def task_func" ascii
        $docstring = "Count the frequency of each word" ascii

        // Key operations
        $regex_pattern = "\\b\\w+\\b" ascii
        $pandas_ops1 = ".value_counts()" ascii
        $pandas_ops2 = "pd.Series" ascii

        // Parameter and return hints
        $param = "text (str):" ascii
        $returns = "Returns:" ascii

    condition:
        // Must have both imports
        $import1 and $import2 and

        // Must have stopwords definition with at least 3 common stopwords
        $stopwords and 2 of ($sw*) and

        // Must have function definition and docstring
        $func_def and $docstring and

        // Must have regex pattern and pandas operations
        $regex_pattern and
        1 of ($pandas_ops*) and

        // Must have parameter and return documentation
        $param and $returns
}
