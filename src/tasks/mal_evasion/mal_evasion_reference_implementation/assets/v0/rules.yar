rule Hello {
    strings:
        $h = "Hello"
    condition:
        $h
}
