rule Data_Exfiltration_Script {
    meta:
        description = "Detects script that encodes and sends data via HTTP POST"
        severity = "high"

    strings:
        // Import statements
        $imp1 = "import requests"
        $imp2 = "import json"
        $imp3 = "import base64"

        // Function definition
        $func = "def task_func"

        // Key operations
        $op1 = "json.dumps"
        $op2 = "base64.b64encode"
        $op3 = "requests.post"
        $op4 = "payload"

        // URL patterns
        $url1 = "http://"
        $url2 = "api-url"

        // Data handling patterns
        $data1 = ".encode("
        $data2 = ".decode("

    condition:
        // Require imports
        all of ($imp*) and

        // Require function definition
        $func and

        // Require at least 3 key operations
        3 of ($op*) and

        // Require URL components
        1 of ($url*) and

        // Require data encoding/decoding
        1 of ($data*)
}
