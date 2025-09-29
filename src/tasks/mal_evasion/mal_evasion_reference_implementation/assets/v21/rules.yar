rule Python_Zip_Creation {
    strings:
        // Key imports
        $import1 = "import os"
        $import2 = "import glob"
        $import3 = "import zipfile"

        // Function definition
        $func = "def task_func"

        // Key strings used in the code
        $str1 = "files.zip"
        $str2 = "Directory"

        // Zip operations
        $zip1 = "zipfile.ZipFile"
        $zip2 = ".write("

        // Error handling
        $error = "FileNotFoundError"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have function definition
        $func and

        // Must have key strings
        all of ($str*) and

        // Must have zip operations
        all of ($zip*) and

        // Must have error handling
        $error
}
