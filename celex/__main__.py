import PIL.Image
from celex import Texture2DPlugin


def main():
    a = PIL.Image.open("deadpan00.data")
    a.save("a.png")

if __name__ == "__main__":
    main()
