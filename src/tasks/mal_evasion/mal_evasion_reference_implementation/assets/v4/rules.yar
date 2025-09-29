rule RandomStatisticsTask
{
    strings:
        // Import statements
        $import1 = "import random"
        $import2 = "import statistics"

        // Key function calls
        $func1 = "random.randint"
        $func2 = "statistics.mean"

        // Characteristic patterns
        $pattern1 = "randint(0, 100)"
        $pattern2 = "random.randint(1, 10)"
        $pattern3 = "sorted_dict"

        // Lambda sorting pattern
        $sort = "sorted" nocase
        $lambda = "lambda" nocase
        $mean = "mean" nocase
        $reverse = "reverse=True"

    condition:
        // Must have both imports
        all of ($import*) and

        // Must have characteristic function calls
        all of ($func*) and

        // Must have at least 2 of the specific patterns
        2 of ($pattern*) and

        // Must have the sorting-related components
        3 of ($sort, $lambda, $mean, $reverse)
}
