rule DataAnalysisProgram {
    strings:
        // Import statements
        $import1 = "import pandas as pd"
        $import2 = "import numpy as np"
        $import3 = "import ast"

        // Key DataFrame operations
        $df1 = "pd.DataFrame"
        $df2 = "pd.read_csv"
        $df3 = ".map"
        $df4 = ".apply"

        // File operations
        $file1 = "os.listdir"
        $file2 = "os.path.join"
        $file3 = ".endswith('.csv')"

        // Column names and operations
        $col1 = "'email'"
        $col2 = "'list'"
        $col3 = "'sum'"
        $col4 = "'mean'"
        $col5 = "'median'"

        // Statistical operations
        $stat1 = "literal_eval"
        $stat2 = "np.mean"
        $stat3 = "np.median"
        $stat4 = ".hist()"

    condition:
        // Must have most of the imports
        2 of ($import*) and

        // Must have DataFrame operations
        2 of ($df*) and

        // Must have file operations
        2 of ($file*) and

        // Must have several of the column names
        3 of ($col*) and

        // Must have statistical operations
        2 of ($stat*)
}
