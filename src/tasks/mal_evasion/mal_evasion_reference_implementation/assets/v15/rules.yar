rule Suspicious_FTP_Downloader {
    meta:
        description = "Detects FTP download script with specific patterns"
        severity = "medium"

    strings:
        // FTP related imports and functions
        $import1 = "import ftplib"
        $import2 = "import subprocess"
        $import3 = "import os"

        // FTP specific function calls
        $ftp1 = "ftplib.FTP"
        $ftp2 = "ftp_obj.login"
        $ftp3 = "ftp_obj.cwd"
        $ftp4 = "ftp_obj.nlst"
        $ftp5 = "ftp_obj.quit"

        // Default credentials and server
        $cred1 = "ftp.dlptest.com"
        $cred2 = "dlpuser"
        $cred3 = "rNrKYTX9g7z3RgJRmxWuGHbeu"

        // Wget command pattern
        $wget = "wget ftp://"

        // Characteristic error messages
        $err1 = "Failed to connect to FTP server"
        $err2 = "Failed to log into FTP server"
        $err3 = "Failed to change to directory"

        // Function and directory patterns
        $func = "def task_func"
        $dir = "downloaded_files"

    condition:
        // Must see multiple indicators to confirm it's this specific script
        (
            // Must have the core imports
            2 of ($import*) and

            // Must have multiple FTP operations
            3 of ($ftp*) and

            // Must have either default credentials or error handling
            (
                2 of ($cred*) or
                2 of ($err*)
            ) and

            // Must have wget and directory creation
            $wget and
            $dir and

            // Must have the main function definition
            $func
        )
}
