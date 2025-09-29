rule TaskFuncIdentifier
{
    strings:
        // Imports
        $import1 = "import itertools"
        $import2 = "from random import shuffle"

        // Function signature and name
        $func = "def task_func"

        // Key variables and operations
        $var1 = "permutations"
        $var2 = "sum_diffs"
        $var3 = "avg_sum_diffs"

        // Mathematical operations
        $math1 = "abs("
        $math2 = "sum("

        // Distinctive docstring content
        $doc1 = "Calculates the average of the sums"
        $doc2 = "absolute differences between"

        // Key code constructs
        $code1 = "itertools.permutations"
        $code2 = "shuffle(perm)"

    condition:
        // Must have both imports
        ($import1 and $import2) and

        // Must have function definition
        $func and

        // Must have at least 2 of the key variables
        2 of ($var*) and

        // Must have both math operations
        all of ($math*) and

        // Must have at least one docstring component
        1 of ($doc*) and

        // Must have at least one key code construct
        1 of ($code*)
}
