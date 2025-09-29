rule TimestampProcessor
{
    strings:
        // Import statements
        $import1 = "from datetime import datetime"
        $import2 = "import pandas as pd"
        $import3 = "import matplotlib.pyplot"

        // Key constants and strings
        $format = "DATE_FORMAT = \"%Y-%m-%d %H:%M:%S\""
        $error = "Input list of timestamps is empty"

        // Function characteristics
        $func = "def task_func"
        $param = "timestamps"

        // DataFrame related
        $col1 = "Timestamp"
        $col2 = "Datetime"

        // Key operations
        $hist = "plt.hist"
        $convert = "datetime.fromtimestamp"
        $df_create = "pd.DataFrame"

    condition:
        // Must have all imports
        all of ($import*) and

        // Must have the date format and error message
        $format and
        $error and

        // Must have function definition and parameter
        $func and
        $param and

        // Must have DataFrame column names
        all of ($col*) and

        // Must have key operations
        $hist and
        $convert and
        $df_create
}
