rule Statistical_Visualization_Code {
    strings:
        // Import statements
        $import1 = "from scipy.stats import zscore"
        $import2 = "matplotlib.pyplot"

        // Statistical functions and terms
        $stat1 = "zscore"
        $stat2 = "fillna"
        $stat3 = "Z-score"

        // Visualization functions
        $viz1 = "hist"
        $viz2 = "tight_layout"

        // DataFrame operations
        $df1 = "DataFrame"
        $df2 = "shape"
        $df3 = "columns"

        // Comments showing statistical intent
        $comment1 = "Calculate Z-scores"
        $comment2 = "Plot histograms"

    condition:
        // Must have both statistical and visualization imports
        ($import1 and $import2) and
        // Must have statistical operations
        (2 of ($stat*)) and
        // Must have visualization functions
        (1 of ($viz*)) and
        // Must have DataFrame operations
        (2 of ($df*)) and
        // Should have statistical/visualization intent in comments
        (1 of ($comment*))
}
