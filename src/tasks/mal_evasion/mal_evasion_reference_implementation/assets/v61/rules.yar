rule File_Size_Reporter {
    meta:
        description = "Detects programs that report file sizes using pandas DataFrame"
        author = "Assistant"

    strings:
        // Import statements
        $import1 = "import pandas" nocase
        $import2 = "import re" nocase
        $import3 = "import os" nocase

        // Key strings
        $pattern = "^EMP"
        $col1 = "File"
        $col2 = "Size"

        // Function components
        $listdir = "os.listdir"
        $getsize = "os.path.getsize"
        $dataframe = "DataFrame"
        $sorted = "sorted"

        // Function signature pattern
        $func_def = /def\s+task_func\s*\(/

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have the characteristic strings
        $pattern and $col1 and $col2 and

        // Must have the key function components
        $listdir and $getsize and $dataframe and $sorted and

        // Must have function definition
        $func_def
}
