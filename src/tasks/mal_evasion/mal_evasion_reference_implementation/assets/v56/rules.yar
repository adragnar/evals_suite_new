rule Python_Histogram_Plotter
{
    strings:
        // Imports
        $import1 = "import random"
        $import2 = "import matplotlib.pyplot"
        $import3 = "import seaborn"

        // Function definition
        $func = "def task_func"

        // Characteristic strings
        $param1 = "from_user"
        $param2 = "colors="
        $colors = /\['b',\s*'g',\s*'r',\s*'c',\s*'m',\s*'y',\s*'k'\]/

        // Plot-related strings
        $plot1 = "plt.figure"
        $plot2 = "sns.histplot"
        $plot3 = "plt.show"

        // Histogram-specific operations
        $hist1 = "color = random.choice"
        $hist2 = "[d['from_user'] for d in result"

    condition:
        // Must have the function definition and imports
        $func and
        2 of ($import*) and

        // Must have plotting-related code
        2 of ($plot*) and

        // Must have some characteristic strings
        (2 of ($param*) or $colors) and

        // Must have histogram-specific operations
        1 of ($hist*)
}
