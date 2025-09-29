rule Python_Math_Combinations_Function {
    meta:
        description = "Detects Python function working with mathematical combinations and logarithms"

    strings:
        // Import statements
        $imp1 = "import math"
        $imp2 = "import itertools"
        $imp3 = "from functools import reduce"

        // Function definition and key variables
        $func = "def task_func"
        $var1 = "sum_log_products"

        // Key function calls and operations
        $op1 = "math.log"
        $op2 = "itertools.combinations"
        $op3 = "reduce(lambda x, y: x * y"

        // Distinctive docstring parts
        $doc1 = "Generates all possible combinations"
        $doc2 = "computes the logarithm of each product"
        $doc3 = "Returns:"
        $doc4 = "float: The sum of the logarithms"

        // Example usage in docstring
        $example = ">>> numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]"

    condition:
        // Must have all imports
        all of ($imp*) and

        // Must have the main function definition
        $func and

        // Must have the key variable
        $var1 and

        // Must have at least 2 of the key operations
        2 of ($op*) and

        // Must have at least 3 of the docstring elements
        3 of ($doc*) and

        // Should have the example
        $example
}
