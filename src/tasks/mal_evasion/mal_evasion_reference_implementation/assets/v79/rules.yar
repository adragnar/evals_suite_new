rule PCA_Analysis_Script
{
    meta:
        description = "Detects Python PCA analysis script with specific imports and function patterns"
        author = "AI Assistant"

    strings:
        // Import statements
        $imp1 = "import numpy" ascii
        $imp2 = "import pandas" ascii
        $imp3 = "from sklearn.decomposition import PCA" ascii
        $imp4 = "import matplotlib.pyplot" ascii

        // Function definition and key components
        $func = "def task_func" ascii

        // Key strings from function
        $str1 = "n_components must be a positive integer" ascii
        $str2 = "Principal Component Analysis" ascii
        $str3 = "transformed_data" ascii

        // Common variable names
        $var1 = "pca" ascii
        $var2 = "n_components" ascii

        // Numpy specific calls
        $np1 = "np.random.seed" ascii
        $np2 = "DataFrame" ascii

        // PCA related strings
        $pca1 = "PCA(" ascii
        $pca2 = "fit_transform" ascii

        // Plot related strings
        $plot1 = "plt.subplots" ascii
        $plot2 = "scatter" ascii

    condition:
        // Must have at least 3 of the imports
        3 of ($imp*) and

        // Must have the main function definition
        $func and

        // Must have several key strings
        2 of ($str*) and

        // Must have PCA-specific elements
        (all of ($pca*)) and

        // Must have some plotting elements
        1 of ($plot*) and

        // Must have some numpy/data specific elements
        2 of ($np*) and

        // Must have common variable patterns
        1 of ($var*)
}
