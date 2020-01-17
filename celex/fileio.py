from typing import List, Callable
from os import walk, path


def all_files(directory: str, recur: bool = True) -> List[str]:
    files: List[str] = []
    for (dirpath, _, filenames) in walk(directory):
        files.extend(path.join(dirpath, f) for f in filenames)
        if not recur:
            break
    return files


def extension_matcher(extension: str) -> Callable[[str], bool]:
    def has_extension(filename: str) -> bool:
        return filename.endswith("." + extension)
    return has_extension


def celeste_datafiles(directory: str) -> List[str]:
    return list(filter(
        extension_matcher("data"),
        all_files(directory)
    ))
