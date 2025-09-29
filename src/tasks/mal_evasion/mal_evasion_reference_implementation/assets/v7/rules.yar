rule Statistical_Dictionary_Generator
{
    strings:
        // Import statements
        $import1 = "import random"
        $import2 = "import math"

        // Function definition
        $func_def = "def task_func"

        // Characteristic operations
        $math1 = "math.sqrt"
        $random1 = "random.randint"
        $range1 = "range(97, 123)"

        // Key variable names and patterns
        $var1 = "random_dict"
        $var2 = "sd_dict"
        $var3 = "LETTERS"

        // Distinctive mathematical patterns
        $math_op = "sum((i - sum(v) / len(v)) ** 2"

        // Common strings from docstring
        $doc1 = "population standard deviation"
        $doc2 = "random integers"

    condition:
        // Must have imports and function definition
        ($import1 and $import2 and $func_def) and

        // Must have at least 2 of the math/random operations
        2 of ($math1, $random1, $range1) and

        // Must have at least 2 of the key variables
        2 of ($var1, $var2, $var3) and

        // Must have mathematical operation or docstring elements
        ($math_op or (1 of ($doc1, $doc2)))
}
