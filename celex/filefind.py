"""
Functions for getting filepaths from the OS.
"""

from os import walk, path
from typing import List, Callable


def extension_matcher(extension: str) -> Callable[[str], bool]:
    """
    Returns a closure that checks if a filename has a certain extension.
    """
    def has_extension(filename: str) -> bool:
        return filename.endswith("." + extension)
    return has_extension


def every(directory: str, recur: bool = True) -> List[str]:
    """
    Finds every file in the argument directory.

    If `recur` is True, files within subdirectories will be searched.
    """
    files: List[str] = []
    for (dirpath, _, filenames) in walk(directory):
        files.extend(path.join(dirpath, f) for f in filenames)
        if not recur:
            break
    return files


def celeste_data(directory: str, recur: bool = True) -> List[str]:
    """
    Finds every Celeste data file in the argument directory.
    """
    return list(filter(
        extension_matcher("data"),
        every(directory, recur)
    ))
