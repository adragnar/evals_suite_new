rule Compression_Base64_Encoder
{
    strings:
        // Import statements
        $import1 = "import base64"
        $import2 = "import json"
        $import3 = "import zlib"

        // Function definition and docstring
        $func_def = "def task_func"
        $doc1 = "Serializes a dictionary to a JSON string"
        $doc2 = "compresses it using zlib"
        $doc3 = "encodes the compressed data with base64"

        // Function calls
        $call1 = "json.dumps"
        $call2 = "zlib.compress"
        $call3 = "base64.b64encode"

    condition:
        // Must find at least 2 imports AND
        // the function name AND
        // at least 2 docstring fragments AND
        // at least 2 function calls
        2 of ($import*) and
        $func_def and
        2 of ($doc*) and
        2 of ($call*)
}
