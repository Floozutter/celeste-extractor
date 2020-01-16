from typing import Tuple, List
from PIL import Image


Size  = Tuple[int, int]            # width, height
Color = Tuple[int, int, int, int]  # red, green, blue, opacity


def to_int(b: bytes) -> int:
    return int.from_bytes(b, "little")


def to_pixels(encoded: bytes) -> (List[Color], Size):
    # read size
    width  = to_int(encoded[0:4])
    height = to_int(encoded[4:8])

    # check if transparency is enabled
    trans = bool(encoded[9])
    trans = False  # hmmm...
    
    # convert run-length encoding to a list of pixels
    pixels = []
    iterbytes = iter(encoded[9:])
    
    reps = next(iterbytes, None)
    while reps is not None:
        if trans:
            o = next(iterbytes)
        else:
            o = 255
        b = next(iterbytes)
        g = next(iterbytes)
        r = next(iterbytes)

        for i in range(reps):
            pixels.append( (r, g, b, o) )

        reps = next(iterbytes, None)
        
    return pixels, (width, height)


def to_image(pixels: List[Color], size: Size) -> Image:
    img = Image.new("RGBA", size)
    img.putdata(pixels)
    return img


def decode(texture2d: bytes) -> Image:
    pixels, size = to_pixels(texture2d)
    return to_image(pixels, size)
