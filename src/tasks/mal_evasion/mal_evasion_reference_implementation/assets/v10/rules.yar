rule Detect_Random_Counter_Program
{
    strings:
        // Import statements
        $imp1 = "from collections import Counter"
        $imp2 = "from random import randint"
        $imp3 = "import itertools"

        // Function signature and key parameters
        $func = "def task_func"
        $param = "RANGE=100"

        // Key operations
        $op1 = "map(int, x)"
        $op2 = "itertools.chain"
        $op3 = "randint(0, RANGE)"
        $op4 = "Counter("

        // Unique docstring fragments
        $doc1 = "Convert elements in 'T1' to integers"
        $doc2 = "Counter: A Counter object representing"

        // Variable names and patterns
        $var1 = "random_nums"
        $var2 = "counts"
        $var3 = "int_list"
        $var4 = "flattened_list"

    condition:
        // Must have all imports
        all of ($imp*) and

        // Must have function definition and at least one parameter
        $func and $param and

        // Must have at least 3 of the key operations
        3 of ($op*) and

        // Must have at least one docstring fragment
        1 of ($doc*) and

        // Must have at least 2 of the variable names
        2 of ($var*)
}
