rule Diabetes_Dataset_Visualization {
    strings:
        // Key imports
        $import1 = "matplotlib.pyplot"
        $import2 = "seaborn"
        $import3 = "pandas"
        $import4 = "sklearn.datasets"

        // Specific dataset and visualization elements
        $dataset = "load_diabetes"
        $viz = "pairplot"
        $font = "Arial"

        // DataFrame operations
        $df1 = "DataFrame"
        $df2 = "columns"
        $df3 = "feature_names"

    condition:
        // Must have the core visualization imports
        2 of ($import*) and

        // Must have dataset loading and visualization
        $dataset and $viz and

        // Must have DataFrame operations
        2 of ($df*) and

        // Must have font configuration
        $font
}
