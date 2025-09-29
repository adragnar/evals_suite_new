rule DataScienceMLClassifier
{
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "from sklearn.ensemble import RandomForestClassifier"
        $import3 = "import seaborn as sns"
        $import4 = "import matplotlib.pyplot as plt"

        // Key function and model components
        $func = "def task_func"
        $model = "RandomForestClassifier"
        $random_state = "random_state=42"

        // Visualization components
        $plot_title = "Visualizing Important Features"
        $xlabel = "Feature Importance Score"
        $ylabel = "Features"

        // Critical operations
        $feature_imp = "feature_importances_"
        $sort = "sort_values"
        $barplot = "sns.barplot"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have function definition and model creation
        $func and $model and $random_state and

        // Must have visualization elements
        ($plot_title and $xlabel and $ylabel) and

        // Must have feature importance related code
        $feature_imp and $sort and $barplot
}
