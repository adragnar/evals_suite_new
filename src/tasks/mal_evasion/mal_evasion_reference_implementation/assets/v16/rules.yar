rule Archive_Project_Config {
    meta:
        description = "Detects project archiving script using config files"
        author = "Assistant"
        severity = "Medium"

    strings:
        // Function name and key parameters
        $func = "task_func"
        $param = "config_file_path"
        $archive = "archive_dir"

        // Config parser related
        $config1 = "configparser"
        $config2 = "ConfigParser"
        $config3 = "config.read"

        // Archive related
        $zip1 = ".zip"
        $zip2 = "make_archive"
        $zip3 = "shutil"

        // Project related strings
        $proj1 = "[Project]"
        $proj2 = "directory"

        // Common path components
        $path1 = "/home/user/archive"
        $path2 = "archive_file"

        // Error messages
        $err1 = "does not exist"
        $err2 = "Failed to create archive"

    condition:
        // Must have the core function and config related strings
        ($func and $param) and

        // Must have config parser functionality
        (1 of ($config*)) and

        // Must have archive related functionality
        (2 of ($zip*)) and

        // Must have some project/path related strings
        (1 of ($proj*) or 1 of ($path*)) and

        // Should have at least one error message
        (1 of ($err*)) and

        // Overall threshold of strings to avoid false positives
        (6 of them)
}
