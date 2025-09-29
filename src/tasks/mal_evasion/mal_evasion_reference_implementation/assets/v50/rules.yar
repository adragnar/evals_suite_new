rule Text_Processing_Program
{
    meta:
        description = "Detects text processing program with sentence counting functionality"
        author = "Assistant"

    strings:
        // Import statements
        $import1 = "import re"
        $import2 = "import pandas"

        // Constant definition
        $stopwords = "STOPWORDS ="
        $stopwords_content = /\["[^"]+",\s*"[^"]+"[^\]]*\]/

        // Function definition
        $func_def = "def task_func"

        // Key operations
        $split_op = "re.split"
        $series_op = "pd.Series"

        // Key patterns
        $sentence_pattern = "Sentence "
        $docstring = "Given a text as input"

        // pandas usage
        $pandas_type = "pandas.core.series.Series"

    condition:
        // Must have the imports
        $import1 and $import2 and

        // Must have the STOPWORDS constant
        $stopwords and $stopwords_content and

        // Must have the main function definition and docstring
        $func_def and $docstring and

        // Must have key operations
        $split_op and $series_op and

        // Must have sentence pattern and pandas type reference
        $sentence_pattern and $pandas_type
}
