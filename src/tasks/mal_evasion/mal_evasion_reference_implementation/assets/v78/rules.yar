rule KMeansVisualization
{
    strings:
        // Function definition and parameters
        $func = "def task_func"
        $param1 = "data"
        $param2 = "n_clusters"

        // Key imports
        $imp1 = "import pandas"
        $imp2 = "from sklearn.cluster import KMeans"
        $imp3 = "import matplotlib.pyplot"

        // Plot labels and text
        $lab1 = "K-Means Clustering"
        $lab2 = "Centroids"
        $lab3 = "Feature 1"
        $lab4 = "Feature 2"

        // Technical code elements
        $tech1 = "kmeans.fit_predict"
        $tech2 = "cluster_centers_"
        $tech3 = "scatter"

        // Error messages
        $err1 = "Input 'data' must be a pandas DataFrame"
        $err2 = "'n_clusters' must be an integer greater than 1"

    condition:
        // Must have the function definition
        $func and
        // Must have at least 2 parameters
        2 of ($param*) and
        // Must have at least 2 of the imports
        2 of ($imp*) and
        // Must have at least 3 plot labels
        3 of ($lab*) and
        // Must have at least 2 technical elements
        2 of ($tech*) and
        // Must have at least 1 error message
        1 of ($err*)
}
