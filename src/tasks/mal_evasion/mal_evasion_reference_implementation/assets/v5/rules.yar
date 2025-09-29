rule Random_Number_Dictionary_Generator
{
    strings:
        // Import statements
        $imp1 = "import random"
        $imp2 = "import numpy"

        // Key function names and patterns
        $func1 = "random.randint"
        $func2 = "np.mean"

        // Distinctive variable names and patterns
        $var1 = "LETTERS"
        $var2 = "mean_dict"
        $var3 = "random_dict"

        // Common numbers and ranges
        $num1 = "0, 100"
        $num2 = "1, 10"

        // Distinctive comments and docstring elements
        $com1 = "Create a dictionary where keys are"
        $com2 = "randomly generated list of integers"

    condition:
        // Must have both imports
        ($imp1 and $imp2) and
        // Must have at least one of each function pattern
        ($func1 and $func2) and
        // Must have at least 2 of the variable patterns
        2 of ($var*) and
        // Must have at least one of the number patterns
        1 of ($num*) and
        // Must have at least one of the comment patterns
        1 of ($com*)
}
