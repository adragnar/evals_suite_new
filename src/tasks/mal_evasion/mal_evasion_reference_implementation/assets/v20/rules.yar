rule CSV_File_Splitter
{
    meta:
        description = "Detects CSV file splitting and shuffling program"
        author = "AI Assistant"

    strings:
        // Key file operation strings
        $csv = ".csv"
        $split_prefix = "split_"

        // Command strings
        $split_cmd = "split"
        $split_args1 = "-n"
        $split_args2 = "-d"

        // Error messages
        $err1 = "Provided file does not exist"
        $err2 = "Provided file is not a CSV"
        $err3 = "An error occurred:"

        // Function and library imports
        $import1 = "subprocess"
        $import2 = "csv"
        $import3 = "glob"
        $import4 = "random"

        // Core operations
        $glob = "glob.glob"
        $shuffle = "random.shuffle"
        $writer = "csv.writer"
        $reader = "csv.reader"

    condition:
        // Must have CSV and split prefix strings
        $csv and $split_prefix and

        // Must have split command components
        $split_cmd and $split_args1 and $split_args2 and

        // Must have at least 2 error messages
        2 of ($err*) and

        // Must have key library imports
        3 of ($import*) and

        // Must have core CSV/file operations
        2 of ($glob, $shuffle, $writer, $reader)
}
