rule Base64_JSON_Timestamp_Encoder {
    strings:
        // Key imports
        $imp1 = "import json"
        $imp2 = "import base64"
        $imp3 = "from datetime import datetime"

        // Key function characteristics
        $func1 = "task_func"
        $func2 = "data['timestamp']"

        // Key operations
        $op1 = "json.dumps"
        $op2 = "base64.b64encode"
        $op3 = ".strftime"
        $op4 = ".decode('ascii')"

        // Format strings
        $fmt1 = "%Y-%m-%d %H:%M:%S"

        // Type hints and docstring elements
        $type1 = "data: dict"
        $type2 = "str: A base64 encoded"

    condition:
        // Must have key imports
        2 of ($imp*) and

        // Must have key function elements
        1 of ($func*) and

        // Must have encoding operations
        2 of ($op*) and

        // Must have either format string or type hints
        (any of ($fmt*) or any of ($type*))
}
