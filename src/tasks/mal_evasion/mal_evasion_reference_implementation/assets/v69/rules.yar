rule Python_Fruit_Sales_Analysis
{
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "import numpy as np"
        $import3 = "import seaborn as sns"

        // Function definition and key parameters
        $func = "def task_func"
        $param1 = "sales_lower_bound"
        $param2 = "sales_upper_bound"

        // Default fruit names
        $fruit1 = "'Apple'"
        $fruit2 = "'Banana'"
        $fruit3 = "'Cherry'"
        $fruit4 = "'Date'"
        $fruit5 = "'Elderberry'"

        // Error messages
        $error1 = "Input must be a pandas DataFrame"
        $error2 = "Input DataFrame must be empty"
        $error3 = "sales_lower_bound must be less than sales_upper_bound"

        // Key function operations
        $op1 = "sns.boxplot"
        $op2 = "itertools.product"
        $op3 = "np.random.randint"

    condition:
        // Must have the core imports
        2 of ($import*) and

        // Must have the function definition and at least one parameter
        $func and 1 of ($param*) and

        // Must have at least 3 of the default fruit names
        3 of ($fruit*) and

        // Must have at least 2 error messages
        2 of ($error*) and

        // Must have at least 2 key operations
        2 of ($op*)
}
