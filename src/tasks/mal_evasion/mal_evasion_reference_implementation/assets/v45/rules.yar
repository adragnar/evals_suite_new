rule Python_DateTime_Visualization {
    strings:
        // Import statements
        $imp1 = "from datetime import datetime"
        $imp2 = "import pandas as pd"
        $imp3 = "import pytz"
        $imp4 = "import matplotlib.pyplot"

        // Constants and key strings
        $date_fmt = "DATE_FORMAT = \"%Y-%m-%d %H:%M:%S\""
        $tz1 = "America/New_York"
        $tz2 = "Europe/London"
        $tz3 = "Asia/Shanghai"

        // Function elements
        $func_name = "def task_func"
        $plot_title = "Datetime = f(Timezone)"
        $df_create = "DataFrame"
        $plt_elements = "plt.ylabel"

    condition:
        // Require multiple matches from different categories to reduce false positives
        2 of ($imp*) and           // At least 2 of the imports
        ($date_fmt) and            // Must have the date format
        2 of ($tz*) and           // At least 2 of the timezones
        2 of ($func_name, $plot_title, $df_create, $plt_elements)  // At least 2 function elements
}
