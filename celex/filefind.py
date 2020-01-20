from typing import List, Callable
from os import walk, path


def extension_matcher(extension: str) -> Callable[[str], bool]:
    def has_extension(filename: str) -> bool:
        return filename.endswith("." + extension)
    return has_extension


def every(directory: str, recur: bool = True) -> List[str]:
    files: List[str] = []
    for (dirpath, _, filenames) in walk(directory):
        files.extend(path.join(dirpath, f) for f in filenames)
        if not recur:
            break
    return files


def celeste_data(directory: str, recur: bool = True) -> List[str]:
    return list(filter(
        extension_matcher("data"),
        every(directory, recur)
    ))
