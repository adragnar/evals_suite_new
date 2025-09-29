rule Command_Output_Processor
{
    strings:
        // File naming pattern
        $output_pattern = "command_"
        $output_ext = "_output.txt"

        // Error messages
        $error1 = "Error executing command, exited with code"
        $error2 = "File '"
        $error3 = "' not found"

        // Common file operation strings
        $dir_check = "output_dir_path"
        $file_check = "commands_file_path"

        // Function signature
        $func_def = "def task_func"

    condition:
        // Must have the output file pattern strings
        ($output_pattern and $output_ext) and

        // Must have at least 2 of the error handling strings
        2 of ($error*) and

        // Must have the path checking variables
        ($dir_check and $file_check) and

        // Must have the function definition
        $func_def
}
