rule Random_String_Character_Counter
{
    strings:
        // Import statements
        $import1 = "import random"
        $import2 = "import string"
        $import3 = "from collections import Counter"

        // Function definition and key parameters
        $func_def = "def task_func"
        $params = "num_strings, string_length"

        // Core functionality strings
        $random_choices = "random.choices"
        $ascii_lower = "string.ascii_lowercase"
        $counter = "character_counter = Counter"
        $most_common = ".most_common()"

        // Unique docstring fragments
        $doc1 = "Creates a list of random strings"
        $doc2 = "counts the frequency of each character"
        $doc3 = "sorted by frequency in descending order"

        // Return type checking from docstring example
        $type_check = "type(task_func(1000, 5)) == list"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have function definition with parameters
        $func_def and $params and

        // Must have core functionality elements
        all of ($random_choices, $ascii_lower, $counter, $most_common) and

        // Must have at least 2 of the docstring elements
        2 of ($doc*) and

        // Must have type checking example
        $type_check
}
