rule Python_Array_Product_Calculator
{
    strings:
        // Import statements
        $import1 = "import numpy as np"
        $import2 = "from functools import reduce"

        // Function components
        $func_def = "def task_func"
        $func_param = "list_of_pairs"

        // Key operations
        $list_comp = "[pair[1] for pair"
        $np_array = "np.array"
        $reduce_mult = "reduce(np.multiply"

        // Documentation elements
        $docstring1 = "Calculate the product of"
        $docstring2 = "numpy.ndarray"
        $docstring3 = "Returns"

    condition:
        // Must have both imports
        ($import1 and $import2) and

        // Must have function definition and parameter
        ($func_def and $func_param) and

        // Must have key operations
        ($list_comp and $np_array and $reduce_mult) and

        // Should have at least 2 docstring elements
        2 of ($docstring*)
}
