from pathlib import Path


def read_files_into_sample(
    current_directory: Path,
    start_directory: Path | None = None,
    files: dict[str, str] | None = None,
    glob_pattern: str = "*",
    destination_folder: Path | None = None,
) -> dict[str, str]:
    """Read files from a directory in a way that preserves the directory structure.

    Args:
    current_directory: The directory to read files from.
    start_directory: The 'top' directory which located file paths are taken relative to.
    files: A dictionary of file names and contents.
    glob_pattern: The pattern to use when searching for files.
    destination_folder: The optional directory to use as the new root when adding files to the sandbox.
    Prepends the relative path. If None, files are added to the sandbox working directory.

    Returns a dictionary of all files in a Sample-friendly format.
    """
    start_directory = current_directory if start_directory is None else start_directory
    files = {} if files is None else files
    for entry in current_directory.glob(glob_pattern):
        if entry.is_dir():
            files = read_files_into_sample(
                current_directory=entry,
                start_directory=start_directory,
                files=files,
                destination_folder=destination_folder,
            )
        else:
            relative_path = entry.relative_to(start_directory)
            file_destination = (
                relative_path
                if destination_folder is None
                else destination_folder / relative_path
            )
            files = files | {str(file_destination): str(entry.absolute())}
    return files
