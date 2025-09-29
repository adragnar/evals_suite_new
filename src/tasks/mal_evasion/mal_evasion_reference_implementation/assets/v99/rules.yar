rule Array_Gzip_Compressor
{
    strings:
        // Import statements
        $imp1 = "import struct"
        $imp2 = "import io"
        $imp3 = "import gzip"

        // Key function components
        $buf = "BytesIO()"
        $gz = "GzipFile"
        $pack = "struct.pack"

        // Function signature
        $func = "def task_func"

        // Array processing indicators
        $arr1 = "newArray"
        $arr2 = ".size"

    condition:
        // Must have all imports
        all of ($imp*) and

        // Must have compression components
        ($buf and $gz) and

        // Must have array processing
        $pack and

        // Must have function definition and array handling
        $func and
        any of ($arr*)
}
