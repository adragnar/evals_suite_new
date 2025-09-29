rule LogFileProcessor
{
    strings:
        // Key imports
        $import1 = "import os"
        $import2 = "import re"

        // Key filesystem operations
        $fs1 = "os.listdir"
        $fs2 = "os.path"
        $fs3 = "getmtime"

        // Path related strings
        $path1 = "/var/log/"

        // Function components
        $func1 = "pattern"
        $func2 = "log_dir"
        $func3 = "log_files"
        $func4 = "sorted"
        $func5 = "lambda"

        // Return statements
        $ret1 = "return None"
        $ret2 = "return os.path.join"

    condition:
        // Must have both imports
        all of ($import*) and

        // Must have filesystem operations
        2 of ($fs*) and

        // Must have default log path
        $path1 and

        // Must have at least 3 of the function components
        3 of ($func*) and

        // Must have at least one return statement pattern
        1 of ($ret*)
}
