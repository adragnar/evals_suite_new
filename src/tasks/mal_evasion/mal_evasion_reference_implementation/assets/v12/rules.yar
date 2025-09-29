rule Python_Statistical_Analysis {
    meta:
        description = "Detects Python script performing statistical analysis with numpy and random numbers"
        author = "AI"
        version = "1.0"

    strings:
        // Import statements
        $imp1 = "import numpy" nocase
        $imp2 = "import itertools" nocase
        $imp3 = "import random" nocase
        $imp4 = "import statistics" nocase

        // Function definition and key strings
        $func = "def task_func" nocase
        $doc1 = "Convert elements in 'T1' to integers"
        $doc2 = "Returns:"
        $doc3 = "tuple: A tuple containing the mean, median, and mode"

        // Key variable names and operations
        $var1 = "random_nums"
        $var2 = "int_list"
        $var3 = "flattened_list"

        // Statistical operations
        $op1 = "np.mean"
        $op2 = "np.median"
        $op3 = "statistics.mode"

        // Function parameters
        $param1 = "T1"
        $param2 = "RANGE"

    condition:
        // Must have at least 3 of the imports
        3 of ($imp*) and

        // Must have the function definition
        $func and

        // Must have at least 2 of the docstring elements
        2 of ($doc*) and

        // Must have at least 2 of the variable names
        2 of ($var*) and

        // Must have at least 2 of the statistical operations
        2 of ($op*) and

        // Must have both parameters
        all of ($param*)
}
