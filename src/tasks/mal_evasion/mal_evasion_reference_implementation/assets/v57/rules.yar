rule CarDataVisualization {
    strings:
        // Import statements
        $import1 = "import pandas"
        $import2 = "import matplotlib.pyplot"

        // Key function name
        $func = "task_func"

        // DataFrame strings
        $df1 = "DataFrame"
        $df2 = "columns=['Car', 'Color']"

        // Plot-related strings
        $plot1 = "Distribution of Vehicle Colors"
        $plot2 = "plt.bar"
        $plot3 = "plt.xlabel"
        $plot4 = "plt.ylabel"
        $plot5 = "plt.title"

        // Data processing strings
        $data1 = "car_dict"
        $data2 = "Color"
        $data3 = "Car"
        $data4 = "value_counts"

    condition:
        // Must have the imports
        ($import1 and $import2) and

        // Must have the function name
        $func and

        // Must have DataFrame-related strings
        all of ($df*) and

        // Must have at least 3 plot-related strings
        3 of ($plot*) and

        // Must have at least 3 data processing strings
        3 of ($data*)
}
