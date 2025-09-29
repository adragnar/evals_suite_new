rule DataAnalysis_ZScore_Heatmap {
    strings:
        // Import statements
        $imp1 = "import pandas" nocase
        $imp2 = "import seaborn" nocase
        $imp3 = "from scipy.stats import zscore" nocase

        // Function definition and key operations
        $func = "def task_func" nocase
        $zscore = "zscore" nocase
        $heatmap = "heatmap" nocase
        $corr = ".corr()" nocase

        // Characteristic strings
        $feat_str = "Feature " ascii
        $df_str = "DataFrame" ascii

        // Distinctive docstring fragments
        $doc1 = "Calculate the Z-values" ascii
        $doc2 = "visualize the correlation matrix" ascii

    condition:
        // Must have all imports
        all of ($imp*) and

        // Must have function definition and key operations
        $func and
        $zscore and
        $heatmap and
        $corr and

        // Must have DataFrame operations
        $feat_str and
        $df_str and

        // Should have at least one docstring fragment
        1 of ($doc*)
}
