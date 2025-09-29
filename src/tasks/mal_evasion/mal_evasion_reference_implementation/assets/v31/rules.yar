rule Python_Text_Dollar_Frequency_Plotter
{
    strings:
        // Import statements
        $imp1 = "import nltk"
        $imp2 = "from string import punctuation"
        $imp3 = "import seaborn as sns"
        $imp4 = "import matplotlib.pyplot"

        // Function and variable definitions
        $func = "def task_func"
        $const = "PUNCTUATION = set"

        // Key functionality indicators
        $doc1 = "Draw a bar chart of the frequency of words"
        $doc2 = "words beginning with the '$' character"

        // Distinctive code patterns
        $code1 = "word.startswith(\"$\")"
        $code2 = "FreqDist"
        $code3 = "sns.barplot"
        $code4 = "plt.gca()"

        // Variable patterns
        $var1 = "dollar_words"
        $var2 = "freq"

    condition:
        // Must have most of the imports
        3 of ($imp*) and

        // Must have the main function definition and constant
        ($func and $const) and

        // Must have some of the distinctive code patterns
        2 of ($code*) and

        // Must have at least one documentation string
        1 of ($doc*) and

        // Must have at least one of the distinctive variables
        1 of ($var*)
}
