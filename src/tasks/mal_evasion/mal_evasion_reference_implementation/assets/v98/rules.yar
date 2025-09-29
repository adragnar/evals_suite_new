rule URL_JSON_Gzip_Processor
{
    strings:
        // Import statements
        $imp1 = "import json"
        $imp2 = "import urllib"
        $imp3 = "import gzip"

        // Key function components
        $func = "def task_func"
        $params = "url_str, file_path"

        // Core operations
        $url_op = "urllib.request.urlopen"
        $json_ops = {6A 73 6F 6E 2E [1-6] 28} // Matches json.X() where X is loads/dumps
        $gzip_op = "gzip.open"

        // File operations
        $gz_ext = ".gz"
        $write_mode = "'wb'"

        // Data processing
        $encode = ".encode()"
        $decode = ".decode()"

    condition:
        // Must have all imports
        all of ($imp*) and

        // Must have function definition with parameters
        $func and $params and

        // Must have core operations
        $url_op and $gzip_op and

        // Must have file handling elements
        $gz_ext and $write_mode and

        // Must have data processing
        ($encode or $decode) and

        // Must have at least one JSON operation
        $json_ops
}
