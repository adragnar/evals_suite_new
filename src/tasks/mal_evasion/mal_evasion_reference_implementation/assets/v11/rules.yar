rule DataVisualizationScript
{
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "import matplotlib.pyplot as plt"
        $import3 = "import seaborn as sns"

        // Key function and docstring elements
        $func = "def task_func"
        $docstring1 = "Create a Pandas DataFrame"
        $docstring2 = "Category vs Value"

        // DataFrame operations
        $df1 = "DataFrame"
        $df2 = "columns=[\"Category\", \"Value\"]"

        // Plotting operations
        $plot1 = "plt.figure"
        $plot2 = "sns.barplot"
        $plot3 = "plt.title"

        // Common variable names
        $var1 = "list_of_pairs"
        $var2 = "Category"
        $var3 = "Value"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have the main function definition
        $func and

        // Must have some docstring elements
        1 of ($docstring*) and

        // Must have DataFrame operations
        all of ($df*) and

        // Must have plotting commands
        2 of ($plot*) and

        // Must have key variable names
        2 of ($var*)
}
