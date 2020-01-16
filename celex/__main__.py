from PIL import Image
from celex import decode


def main():
    with open("deadpan00.data", "rb") as ifile:
        a = decode.decode(ifile.read())
    a.save("a.png")


if __name__ == "__main__":
    main()
