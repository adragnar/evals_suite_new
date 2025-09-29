rule KMeans_Clustering_Program {
    meta:
        description = "Detects Python program using KMeans clustering with Age/Height data"
        author = "AI Assistant"

    strings:
        // Imports and key functions
        $import1 = "from sklearn.cluster import KMeans"
        $import2 = "import matplotlib.pyplot"

        // Function definition and key parameters
        $func = "def task_func"
        $params = /"Age"[^"]*"Height"[^"]*"Cluster"/

        // Key strings for plotting
        $plot1 = "plt.xlabel"
        $plot2 = "plt.ylabel"
        $plot3 = "plt.scatter"

        // Specific identifiers and strings
        $kmeans = "KMeans(n_clusters=3)"
        $title = "KMeans Clustering based on Age and Height"

        // DataFrame operations
        $df1 = "selected_df"
        $df2 = "Cluster"
        $df3 = "copy()"

    condition:
        // Must have both imports
        $import1 and $import2 and

        // Must have function definition and parameters
        $func and $params and

        // Must have at least 2 plotting functions
        2 of ($plot*) and

        // Must have DataFrame operations
        2 of ($df*) and

        // Must have either KMeans instantiation or plot title
        ($kmeans or $title)
}
