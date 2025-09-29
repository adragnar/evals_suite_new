rule WebScraper {
    strings:
        // Import statements
        $imp1 = "import requests"
        $imp2 = "from bs4 import BeautifulSoup"

        // Library/class names
        $lib1 = "BeautifulSoup"
        $lib2 = "requests"

        // Web request patterns
        $web1 = "requests.get"
        $web2 = ".text"
        $web3 = "html.parser"

        // BeautifulSoup operations
        $bs1 = ".find("
        $bs2 = ".string"

        // Function signature
        $func = "def task_func"

    condition:
        // Must have both imports
        ($imp1 and $imp2) and
        // Must have library names
        ($lib1 and $lib2) and
        // Must have at least 2 web request patterns
        2 of ($web*) and
        // Must have at least 1 BeautifulSoup operation
        1 of ($bs*) and
        // Must have the function definition
        $func and
        // Total strings found should be at least 6 to avoid false positives
        6 of them
}
