rule Random_String_Counter
{
    strings:
        // Import statements
        $import1 = "import collections"
        $import2 = "import random"
        $import3 = "import string"

        // Function definition and key components
        $func = "def task_func"
        $counter = "collections.Counter"
        $choices = "random.choices"

        // Key string literals
        $ascii1 = "string.ascii_uppercase"
        $ascii2 = "string.ascii_lowercase"
        $error = "ValueError"

        // Characteristic code patterns
        $join = "'.join"
        $dict = "dict("

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have the function definition
        $func and

        // Must have at least 4 of the other characteristic strings
        4 of ($counter, $choices, $ascii1, $ascii2, $error, $join, $dict)
}
