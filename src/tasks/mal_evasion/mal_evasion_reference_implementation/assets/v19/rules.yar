rule Process_Manager_Script {
    strings:
        // Import statements
        $import1 = "import subprocess"
        $import2 = "import psutil"
        $import3 = "import time"

        // Key function calls
        $func1 = "process_iter"
        $func2 = "terminate"
        $func3 = "Popen"
        $func4 = "sleep"

        // Distinctive string patterns
        $msg1 = "Process not found. Starting"
        $msg2 = "Process found. Restarting"

        // Function definition pattern
        $def = "def task_func"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have the function definition
        $def and

        // Must have the key function calls
        all of ($func*) and

        // Must have both message patterns
        all of ($msg*) and

        // Ensure reasonable file size to avoid false positives
        filesize < 5KB
}
