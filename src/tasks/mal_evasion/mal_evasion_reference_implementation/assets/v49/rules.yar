rule TextAnalysisDTM
{
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "import regex as re"
        $import3 = "from sklearn.feature_extraction.text import CountVectorizer"

        // Key function and class names
        $func = "def task_func"
        $class = "CountVectorizer"

        // Key method calls
        $method1 = "fit_transform"
        $method2 = "get_feature_names_out"

        // Core variable names
        $var1 = "vectorizer"
        $var2 = "dtm"
        $var3 = "DataFrame"

        // Key operations
        $op1 = "re.split"
        $op2 = "dtm.toarray"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have the main function definition
        $func and

        // Must have the key class name
        $class and

        // Must have at least 4 of the other identifying features
        4 of ($method*, $var*, $op*)
}
