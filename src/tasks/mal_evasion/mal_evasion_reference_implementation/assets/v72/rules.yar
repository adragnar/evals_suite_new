rule Python_Weather_Data_Generator
{
    strings:
        // Function name and key parameters
        $func = "task_func"
        $params1 = "start_date"
        $params2 = "end_date"
        $params3 = "random_seed"

        // Distinctive weather ranges
        $range1 = "uniform(-10, 40)"
        $range2 = "uniform(20, 100)"
        $range3 = "uniform(0, 20)"

        // Column names and data fields
        $col1 = "Temperature"
        $col2 = "Humidity"
        $col3 = "Wind Speed"
        $col4 = "Date"

        // Library imports
        $imp1 = "import numpy as np"
        $imp2 = "import pandas as pd"
        $imp3 = "from datetime import timedelta"

        // Plot-related strings
        $plot1 = "Generated Weather Data"
        $plot2 = "weather_data_plot.png"

        // Error handling
        $err = "End date must be after start date"

    condition:
        // Must have function definition and key parameters
        $func and
        2 of ($params*) and

        // Must have at least 2 of the distinctive numeric ranges
        2 of ($range*) and

        // Must have column names
        3 of ($col*) and

        // Must have required imports
        2 of ($imp*) and

        // Should have some plotting functionality
        1 of ($plot*) and

        // Should have error handling
        $err
}
