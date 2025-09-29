rule DataAnalysisScript {
    strings:
        // Import statements
        $import1 = "import numpy" nocase
        $import2 = "import seaborn" nocase

        // Library aliases
        $np = "np"
        $sns = "sns"

        // Statistical operations
        $stat1 = "mean" nocase
        $stat2 = "describe" nocase
        $stat3 = "fillna" nocase

        // Plotting functions
        $plot1 = "displot" nocase
        $plot2 = "bins" nocase

        // DataFrame operations
        $df1 = "DataFrame" nocase
        $df2 = "select_dtypes" nocase

        // Common statistical terms in output
        $out1 = "count"
        $out2 = "std"
        $out3 = "min"
        $out4 = "max"

    condition:
        // Must have the imports
        ($import1 and $import2) and
        // Must have library aliases
        ($np and $sns) and
        // Must have at least 2 statistical operations
        2 of ($stat*) and
        // Must have plotting elements
        all of ($plot*) and
        // Must have DataFrame operations
        1 of ($df*) and
        // Must have at least 3 statistical output terms
        3 of ($out*)
}
