"""
Parse command-line arguments to extract Celeste data files.
"""

from argparse import ArgumentParser, ArgumentTypeError
from os import path

from celex import filefind
from celex import decode

from typing import Tuple


def extract(inputdir: str, outputdir: str) -> None:
    """
    Extract Celeste data files from `inputdir` to `outputdir`.

    Extracted files are saved to `outputdir` as PNG files.
    Progress is printed to the console.
    """
    print(f"Extracting Celeste data files from:\n\t{inputdir}")
    print(f"Saving extracted files to:\n\t{outputdir}")
    datafilepaths = filefind.celeste_data(inputdir)
    total = len(datafilepaths)
    counter = 0
    for dfp in datafilepaths:
        filename = path.relpath(dfp, inputdir) \
            .replace(".data", ".png") \
            .replace("\\", ".") \
            .replace( "/", ".")
        print(f"Creating: {filename}")
        try:
            with open(dfp, "rb") as datafile:
                img = decode.decode(datafile.read())
                img.save(path.join(outputdir, filename), "PNG")
            counter += 1
        except Exception as e:
            print(f"\tSkipping due to {e}")
    print(f"Finished: {counter} of {total} successfully extracted")


def valid_dir(directory: str) -> str:
    """
    Check if an argparse argument is a valid path to a directory.
    """
    if not path.isdir(directory):
        msg = f"{directory} is not a valid path to a directory"
        raise ArgumentTypeError(msg)
    return directory

def parse_args() -> Tuple[str, str]:
    """
    Get input and output directory args from the command line.
    """
    parser = ArgumentParser(description="Extract Celeste data files",
                            prog="celex")
    parser.add_argument("inputdir", type=valid_dir,
                        help="directory containing Celeste data files")
    parser.add_argument("outputdir", type=valid_dir,
                        nargs="?", default="./output",
                        help="directory to save extracted PNG files to")
    args = parser.parse_args()
    return args.inputdir, args.outputdir
    

if __name__ == "__main__":
    extract(*parse_args())
