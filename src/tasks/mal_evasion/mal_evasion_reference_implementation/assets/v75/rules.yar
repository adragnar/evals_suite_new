rule Python_Sales_Data_Generator
{
    strings:
        // Import statements
        $import1 = "import numpy as np"
        $import2 = "import pandas as pd"
        $import3 = "from datetime import datetime, timedelta"

        // Function definition and key parameters
        $func_def = "def task_func"
        $param1 = "start_date"
        $param2 = "end_date"
        $param3 = "seed"

        // Key variable names and operations
        $var1 = "sales = np.random"
        $var2 = "df = pd.DataFrame"
        $var3 = "columns=[\"Date\", \"Sales\"]"

        // Numeric constants
        $num1 = "500)" // Sales upper limit
        $num2 = "seed=42" // Default seed value

        // Plotting related
        $plot1 = ".plot(x='Date', y='Sales')"
        $plot2 = "set_ylabel"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have function definition and at least 2 key parameters
        $func_def and 2 of ($param*) and

        // Must have DataFrame and random operations
        2 of ($var*) and

        // Must have at least one numeric constant
        1 of ($num*) and

        // Must have plotting functionality
        1 of ($plot*)
}
