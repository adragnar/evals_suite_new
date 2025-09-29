rule Backup_Script_Logger {
    meta:
        description = "Detects backup script logging program with JSON output"
        author = "Assistant"
        severity = "Info"

    strings:
        // File path strings
        $path1 = "backup.sh"
        $path2 = "backup_log.json"

        // Format strings
        $fmt1 = "%Y-%m-%d %H:%M:%S"

        // JSON field names
        $json1 = "start_time"
        $json2 = "end_time"
        $json3 = "exit_status"

        // Error messages
        $err1 = "Script " ascii
        $err2 = "does not exist" ascii
        $err3 = "Failed to run" ascii

        // Function related
        $func1 = "task_func"
        $func2 = "subprocess"
        $func3 = "json.dump"

    condition:
        // Must have:
        // - At least one path string
        // - The datetime format string
        // - At least 2 JSON field names
        // - At least 2 error messages
        // - At least 2 function indicators
        (any of ($path*)) and
        $fmt1 and
        (2 of ($json*)) and
        (2 of ($err*)) and
        (2 of ($func*))
}
