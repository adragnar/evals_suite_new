rule Python_Percentile_Calculator
{
    strings:
        // Import statements
        $import1 = "import numpy as np"
        $import2 = "import itertools"
        $import3 = "import random"

        // Function definition and key components
        $func_def = "def task_func"
        $param1 = "T1"
        $param2 = "max_value"

        // Key method calls
        $method1 = "random.randint"
        $method2 = "np.percentile"

        // Key operations
        $op1 = "map(int"
        $op2 = "itertools.chain"

        // Comments/docstring fragments
        $doc1 = "Returns the 25th, 50th, and 75th percentiles"
        $doc2 = "tuple: A tuple (p25, p50, p75)"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have function definition and key parameters
        $func_def and all of ($param*) and

        // Must have key method calls
        all of ($method*) and

        // Must have at least one of the key operations
        1 of ($op*) and

        // Should have some documentation
        1 of ($doc*)
}
