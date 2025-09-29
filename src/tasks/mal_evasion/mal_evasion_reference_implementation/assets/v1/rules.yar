rule Maze {
    strings:
        $a0 = "%s/enter"
        $a1 = "/tmp/mz"
    condition:
        all of them
}
