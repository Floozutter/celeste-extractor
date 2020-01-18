from celex import decode
from celex import fileio

from PIL import Image
from os import path


def main():
    dirpath = input("Path to the Celeste graphics directory: ")
    filepaths = fileio.celeste_datafiles(dirpath)
    for fp in filepaths:
        fname = path.relpath(fp, dirpath) + ".png"
        fname = fname.replace("/", ".")
        fname = fname.replace("\\", ".")
        print(fname)
        with open(fp, "rb") as ifile:
            try:
                img = decode.decode(ifile.read())
                img.save("./output/" + fname)
            except MemoryError:
                print("\Skipping due to out of memory!")


if __name__ == "__main__":
    main()
