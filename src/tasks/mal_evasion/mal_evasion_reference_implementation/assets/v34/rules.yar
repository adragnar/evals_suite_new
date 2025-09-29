rule Python_DataViz_TaskFunc {
    strings:
        // Import statements
        $imp1 = "import seaborn as sns"
        $imp2 = "import matplotlib.pyplot as plt"

        // Function name and key parameters
        $func = "def task_func"
        $param1 = "target_values=[1, 3, 4]"

        // Distinctive docstring content
        $doc1 = "Replace all elements in DataFrame columns"
        $doc2 = "Returns:"
        $doc3 = "matplotlib.axes.Axes"

        // Key function calls and operations
        $plot1 = "sns.kdeplot"
        $plot2 = "plt.figure"
        $plot3 = "plt.legend"

        // DataFrame operations
        $df1 = "df.applymap"
        $df2 = "df.columns"

    condition:
        // Must have imports
        ($imp1 and $imp2) and

        // Must have function definition and params
        $func and $param1 and

        // Must have at least 2 docstring elements
        2 of ($doc*) and

        // Must have plotting commands
        2 of ($plot*) and

        // Must have DataFrame operations
        1 of ($df*)
}
