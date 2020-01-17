from celex import decode
from celex import fileio

from PIL import Image
from ntpath import basename


def main():
    dirpath = input("Path to the Celeste graphics directory: ")
    filepaths = fileio.celeste_datafiles(dirpath)
    for path in filepaths:
        print(path)
        with open(path, "rb") as ifile:
            try:
                img = decode.decode(ifile.read())
                img.save("./output/" + basename(path) + ".png")
            except MemoryError:
                print("\tOops, out of memory!")
            except StopIteration:
                print("\tOops, bad code!")


if __name__ == "__main__":
    main()
