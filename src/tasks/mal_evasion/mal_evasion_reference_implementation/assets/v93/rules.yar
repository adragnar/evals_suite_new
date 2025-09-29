rule GradeCalculatorProgram {
    meta:
        description = "Detects grade calculation program with pandas/numpy"
        author = "AI Assistant"

    strings:
        // Import statements
        $imp1 = "import pandas as pd"
        $imp2 = "import numpy as np"
        $imp3 = "from random import randint"

        // Constant definitions and key variables
        $const1 = "STUDENTS = ["
        $const2 = "COURSES = ["

        // Function name and key components
        $func = "def task_func"
        $doc = "Generates a DataFrame containing random grades"

        // Characteristic student and course names
        $student1 = "'Joe'"
        $student2 = "'Amy'"
        $course1 = "'Math'"
        $course2 = "'Physics'"

        // DataFrame operations
        $df1 = "DataFrame"
        $df2 = "Average Grade"
        $df3 = "grades_df"

    condition:
        // Must find imports and function definition
        all of ($imp*) and $func and

        // Must find some constant definitions and DataFrame usage
        ($const1 or $const2) and 2 of ($df*) and

        // Must find some characteristic data values
        (1 of ($student*) or 1 of ($course*)) and

        // Must find docstring
        $doc
}
