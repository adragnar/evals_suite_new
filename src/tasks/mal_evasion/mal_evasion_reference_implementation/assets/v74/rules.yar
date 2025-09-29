rule Product_Rating_Generator
{
    strings:
        // Function name and signature
        $func_def = "def task_func"

        // Key imports
        $imp1 = "import pandas as pd"
        $imp2 = "from random import choices, seed"

        // Key pandas operations
        $df1 = "DataFrame"
        $df2 = "sort_values"
        $df3 = "columns="

        // Function parameters
        $param1 = "products"
        $param2 = "ratings"
        $param3 = "weights"
        $param4 = "random_seed"

        // Key operations
        $op1 = "choices"
        $op2 = "seed"
        $op3 = "ascending=False"

    condition:
        // Must have function definition and both imports
        $func_def and $imp1 and $imp2 and

        // Must have at least 2 DataFrame operations
        2 of ($df*) and

        // Must have at least 3 of the parameters
        3 of ($param*) and

        // Must have at least 2 key operations
        2 of ($op*)
}
