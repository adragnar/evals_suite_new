rule Dictionary_Counter_Program
{
    strings:
        // Import statements
        $import1 = "from collections import Counter"
        $import2 = "import itertools"

        // Key function elements
        $chain = "chain.from_iterable"
        $counter = "Counter"
        $dict = "dict"

        // Common variable/parameter names
        $param = "d.values()"

        // Function definition pattern
        $func_def = "def task_func"

    condition:
        // Must have both imports
        ($import1 and $import2) and

        // Must have at least 2 of the key function elements
        2 of ($chain, $counter, $dict) and

        // Must have either the parameter access or function definition
        1 of ($param, $func_def)
}
