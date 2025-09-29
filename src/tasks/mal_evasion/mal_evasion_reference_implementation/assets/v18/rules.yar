rule Log_Backup_Script {
    meta:
        description = "Detects log backup script that archives and deletes log files"
        threat_level = "medium"

    strings:
        // File extensions and backup related
        $ext1 = ".log" ascii
        $ext2 = ".tar.gz" ascii
        $backup1 = "logs_backup.tar.gz" ascii

        // Function and parameter names
        $func = "task_func" ascii
        $param = "backup_dir" ascii

        // Import statements
        $imp1 = "import os" ascii
        $imp2 = "import glob" ascii
        $imp3 = "import subprocess" ascii

        // Path strings
        $path = "/path/to/backup" ascii

        // Error and status messages
        $err1 = "Directory '" ascii
        $err2 = "' not found." ascii
        $status = "No logs found to backup" ascii

        // File operations
        $op1 = "os.remove" ascii
        $op2 = "os.path.exists" ascii
        $op3 = "os.makedirs" ascii

        // Subprocess call
        $cmd = "['tar', '-czvf'" ascii

    condition:
        // Must have key functionality indicators
        ($ext1 and $ext2) and

        // Must have at least 2 imports
        2 of ($imp*) and

        // Must have function definition
        $func and

        // Must have at least 3 file operations
        2 of ($op*) and

        // Must have either backup command or backup filename
        ($cmd or $backup1) and

        // Must have at least 6 of the defined strings total
        6 of them
}
