rule Python_Iris_Visualization {
    meta:
        description = "Detects Python script for Iris dataset visualization using seaborn pairplot"
        author = "AI Assistant"
        severity = "Info"

    strings:
        // Import statements
        $import1 = "import matplotlib.pyplot" nocase
        $import2 = "import pandas" nocase
        $import3 = "import seaborn" nocase
        $import4 = "from sklearn.datasets import load_iris" nocase

        // Function and variable patterns
        $func = "def task_func" nocase
        $iris = "load_iris()" nocase
        $pairplot = "sns.pairplot" nocase

        // Specific visualization elements
        $plot1 = "Iris Dataset Pair Plot" nocase
        $plot2 = "plt.rc('font'" nocase

        // Docstring content
        $doc1 = "Draws a seaborn pair plot" nocase
        $doc2 = "iris dataset" nocase

        // Dataset specifics
        $col1 = "sepal length" nocase
        $col2 = "petal length" nocase

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have function definition and iris dataset loading
        $func and $iris and

        // Must have plotting elements
        $pairplot and

        // Must have at least one plot title/font reference
        1 of ($plot*) and

        // Must have some docstring content
        1 of ($doc*) and

        // Must have at least one dataset column reference
        1 of ($col*)
}
