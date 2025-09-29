rule StudentScoreGenerator
{
    strings:
        // Import statements
        $imp1 = "import numpy" nocase
        $imp2 = "import pandas" nocase

        // Function definition and key parameters
        $func = "def task_func"
        $param1 = "students="
        $param2 = "seed="

        // Distinctive string arrays
        $student1 = "Alice"
        $student2 = "Bob"
        $student3 = "Charlie"
        $student4 = "David"
        $student5 = "Eve"

        // DataFrame operations
        $col1 = "Student"
        $col2 = "Score"

        // Plotting commands
        $plot1 = "plot(x='Student', y='Score'"
        $plot2 = "kind='bar'"

    condition:
        // Must have both imports
        ($imp1 and $imp2) and

        // Must have function definition and at least one parameter
        $func and ($param1 or $param2) and

        // Must have at least 3 of the student names
        3 of ($student1, $student2, $student3, $student4, $student5) and

        // Must have DataFrame column names
        ($col1 and $col2) and

        // Must have at least one plotting command
        ($plot1 or $plot2)
}
