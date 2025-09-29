rule Numeric_List_Processing {
    strings:
        // Imports
        $import1 = "import numpy as np"
        $import2 = "from itertools import zip_longest"

        // Function definition and parameters
        $func = "def task_func"
        $param1 = "l1"
        $param2 = "l2"
        $param3 = "THRESHOLD"

        // Distinctive operations and variables
        $var1 = "combined"
        $var2 = "differences"
        $var3 = "closest_index"

        // Numpy operations
        $np1 = "np.abs"
        $np2 = "np.array"
        $np3 = "np.argmin"

        // Distinctive value
        $threshold = "0.5"

    condition:
        // Must have both imports
        all of ($import*) and

        // Must have function definition and at least 2 of the parameters
        $func and 2 of ($param*) and

        // Must have at least 2 of the distinctive variables
        2 of ($var*) and

        // Must have at least 2 numpy operations
        2 of ($np*) and

        // Should have the default threshold value
        $threshold
}
