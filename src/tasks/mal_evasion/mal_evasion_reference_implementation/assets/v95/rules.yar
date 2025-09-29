rule File_Type_Scanner
{
    strings:
        // Imports
        $import1 = "import re"
        $import2 = "import os"
        $import3 = "import glob"
        $import4 = "import mimetypes"

        // Function signature
        $func_def = "def task_func"
        $params = "directory, file_pattern, suffix"

        // Key operations
        $chdir = "os.chdir"
        $glob = "glob.glob"
        $search = "re.search"
        $mime = "mimetypes.guess_type"

        // Distinctive variables and operations
        $file_types = "file_types"
        $dict_ret = "return file_types"

        // Docstring elements
        $doc1 = "Scans a specified directory for files"
        $doc2 = "MIME types"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have function definition with parameters
        $func_def and $params and

        // Must have at least 3 of the key operations
        3 of ($chdir, $glob, $search, $mime) and

        // Must have dictionary operations
        all of ($file_types, $dict_ret) and

        // Must have some docstring elements
        1 of ($doc*)
}
