rule DataScienceStandardization
{
    strings:
        // Import statements
        $import1 = "from sklearn.preprocessing import StandardScaler"
        $import2 = "import seaborn as sns"
        $import3 = "import matplotlib.pyplot"

        // Function definition and key components
        $func_def = "def task_func"
        $docstring = "Standardize numeric columns in a DataFrame"

        // Key operations
        $fillna = "fillna"
        $mean = ".mean"
        $standardscaler = "StandardScaler()"
        $fit_transform = "fit_transform"
        $heatmap = "sns.heatmap"

        // DataFrame operations
        $df_cols = "df[df.columns]"
        $corr = ".corr()"

        // Return statement
        $return = "return df, heatmap"

    condition:
        // Require multiple matches to reduce false positives
        // Must have at least 2 imports
        2 of ($import*) and
        // Must have function definition and either docstring or key DataFrame operations
        $func_def and
        (
            $docstring or
            // Must have at least 3 key operations
            3 of ($fillna, $mean, $standardscaler, $fit_transform, $heatmap, $df_cols, $corr)
        ) and
        // Must have return statement
        $return
}
