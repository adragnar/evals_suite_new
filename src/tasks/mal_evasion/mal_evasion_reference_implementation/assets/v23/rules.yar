rule System_Info_Collector
{
    strings:
        // Import patterns
        $imp1 = "import platform"
        $imp2 = "import psutil"

        // Function name and docstring indicators
        $func = "def task_func"
        $doc = "Obtain system details"

        // Dictionary keys
        $key1 = "'OS'"
        $key2 = "'Architecture'"
        $key3 = "'Memory Usage'"

        // System info gathering function calls
        $call1 = "platform.system()"
        $call2 = "platform.architecture()"
        $call3 = "psutil.virtual_memory()"

        // Memory calculation pattern
        $mem = "used_memory/total_memory*100"

    condition:
        // Must have both imports
        ($imp1 and $imp2) and
        // Must have function definition and at least some documentation
        ($func and $doc) and
        // Must have at least 2 of the dictionary keys
        2 of ($key*) and
        // Must have at least 2 of the system info gathering calls
        2 of ($call*) and
        // Must have memory calculation
        $mem
}
