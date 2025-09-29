rule DataScienceNormalizationPlot
{
    strings:
        // Import statements
        $import1 = "from sklearn.preprocessing import MinMaxScaler"
        $import2 = "import matplotlib.pyplot"

        // Function and variable names
        $func = "task_func"
        $var1 = "MinMaxScaler"
        $var2 = "boxplot"

        // Plot configuration strings
        $plot1 = "grid=False"
        $plot2 = "vert=False"
        $plot3 = "fontsize=15"

        // Documentation strings
        $doc1 = "Normalize numeric columns"
        $doc2 = "box plot"
        $doc3 = "Missing values are replaced"

    condition:
        // Must have both imports
        ($import1 and $import2) and

        // Must have function name and key variables
        $func and ($var1 or $var2) and

        // Must have at least 2 plotting configs
        2 of ($plot*) and

        // Must have at least 2 doc strings
        2 of ($doc*)
}
