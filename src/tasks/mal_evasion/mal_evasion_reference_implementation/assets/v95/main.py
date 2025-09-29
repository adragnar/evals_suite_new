import re
import os
import glob
import mimetypes


def task_func(directory, file_pattern, suffix):
    """
    Scans a specified directory for files matching a given pattern and with a certain suffix, then determines their file types.
    The function returns a dictionary with file names as keys and their corresponding MIME types as values.

    Parameters:
        directory (str): The path to the directory to scan.
        file_pattern (str): The pattern to match files against.
        suffix (str): The suffix that files must have to be included.

    Returns:
        dict: A dictionary mapping file names to their MIME types.

    Requirements:
    - re
    - os
    - glob
    - mimetypes

    Examples:
    >>> isinstance(task_func(r'dir', '*', '_suff), dict)
    True
    >>> 'example_suff.txt' in task_func(r'dir', '*_suff.txt', '_suff')
    True  # This example assumes 'example_suff.txt' is in the directory and matches the pattern and suffix
    """

    os.chdir(directory)
    files = glob.glob(file_pattern)
    file_types = {}

    for file in files:
        if re.search(suffix, file):
            file_type = mimetypes.guess_type(file)[0]
            file_types[file] = file_type

    return file_types
