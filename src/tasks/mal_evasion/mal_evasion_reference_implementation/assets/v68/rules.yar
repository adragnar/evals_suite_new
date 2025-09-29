rule IP_Geolocation_Tool {
    meta:
        description = "Detects IP geolocation lookup tool using ipinfo.io"
        author = "Assistant"
        severity = "Info"

    strings:
        // API and error strings
        $api_url = "https://ipinfo.io/"
        $error_msg1 = "Host must be a non-empty string"
        $error_msg2 = "Failed to retrieve information for"

        // Function names and key variables
        $func_name = "task_func"
        $var1 = "ip_address"
        $var2 = "geolocation"

        // Import indicators
        $imp1 = "import socket"
        $imp2 = "import requests"

        // Socket operation
        $socket_op = "gethostbyname"

    condition:
        // Must have API URL and at least one error message
        $api_url and
        1 of ($error_msg*) and

        // Must have either both imports or socket operation
        (all of ($imp*) or $socket_op) and

        // Must have at least 2 of the variable/function names
        2 of ($var*, $func_name)
}
