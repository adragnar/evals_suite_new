rule Salary_Distribution_Analysis {
    strings:
        // Key string literals
        $title = "Salary Distribution in EMPXX Department"
        $xlabel = "Salary"
        $ylabel = "Number of Employees"

        // Department code pattern
        $dept = "EMPXX"

        // Required imports
        $import1 = "import random"
        $import2 = "import matplotlib.pyplot"

        // Salary range constants
        $salary_min = "20000"
        $salary_max = "100000"

        // Common plotting functions
        $plot1 = "plt.hist"
        $plot2 = "plt.title"
        $plot3 = "plt.xlabel"
        $plot4 = "plt.ylabel"

    condition:
        // Must have the title and axis labels
        $title and $xlabel and $ylabel and

        // Must have department code
        $dept and

        // Must have both imports
        $import1 and $import2 and

        // Must have salary range values
        $salary_min and $salary_max and

        // Must have at least 3 of the plotting functions
        3 of ($plot*)
}
