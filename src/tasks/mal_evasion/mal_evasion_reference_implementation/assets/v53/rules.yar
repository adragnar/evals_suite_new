rule NormalDistPlotter
{
    strings:
        // Import statements
        $imp1 = "import numpy as np"
        $imp2 = "from scipy import stats"
        $imp3 = "import matplotlib.pyplot"

        // Key strings
        $title = "Normal Distribution"

        // Function definition and parameters
        $func = "def task_func"
        $param1 = "mu"
        $param2 = "sigma"
        $param3 = "num_samples"

        // Key method calls
        $m1 = "random.normal"
        $m2 = "hist"
        $m3 = "norm.pdf"

    condition:
        // Require imports
        2 of ($imp*) and

        // Require title string
        $title and

        // Require function definition with parameters
        $func and 2 of ($param*) and

        // Require at least 2 key method calls
        2 of ($m*)
}
