"""
Functions for decoding the bytes of a Celeste data file.
"""

from PIL import Image
from typing import Tuple

Size = Tuple[int, int]  # width, height


def bytes_to_int(b: bytes) -> int:
    """
    Convert bytes to an int, with hardcoded Endianness.
    """
    return int.from_bytes(b, "little")


def data_to_rgba(data: bytes) -> Tuple[bytes, Size]:
    """
    Convert Celeste data bytes to RGBA bytes and a size.

    Celeste data files have two parts, a header then pixel data.
    The header describes the data in this order:
        - image width  (4 byte integer)
        - image height (4 byte integer)
        - transparency (1 byte boolean)
        
    The pixel data uses a run-length encoding (RLE).
    A run of pixels is encoded in groups of bytes following this order:
        - length of the run of pixels (1 byte integer)
        - A, alpha channel / opacity  (1 byte integer)
        - B, blue color channel       (1 byte integer)
        - G, green color channel      (1 byte integer)
        - R, red color channel        (1 byte integer)

    The pixel data omits encoding redundant information in some cases.
    If the transparency byte is False, the alpha channel byte is omitted.
    If the alpha channel byte is 0, the RGB bytes are omitted.
    """

    # read size
    width  = bytes_to_int(data[0:4])
    height = bytes_to_int(data[4:8])

    # check if transparency is enabled
    trans = bool(data[8])
    
    # prepare to convert run-length encoding to raw
    rgba = bytearray()
    iterbytes = iter(data[9:])
    
    while True:
        # get run-length byte, or reach the end
        runlength = next(iterbytes, None)

        if runlength is None:  # no more bytes to read
            break

        # get alpha channel byte
        if trans:
            a = next(iterbytes)
        else:
            a = 255

        # get color bytes
        if a == 0:  # color bytes aren't encoded
            b = 0
            g = 0
            r = 0
        else:
            b = next(iterbytes)
            g = next(iterbytes)
            r = next(iterbytes)

        # write to rgba bytearray
        for i in range(runlength):
            rgba.extend(bytes( (r, g, b, a) ))
        
    return bytes(rgba), (width, height)


def rgba_to_image(rgba: bytes, size: Size) -> Image.Image:
    """
    Convert RGBA bytes and a size to a PIL.Image.Image.
    """
    return Image.frombytes("RGBA", size, rgba)


def decode(data: bytes) -> Image.Image:
    """
    Create a PIL.Image.Image from the bytes of a Celeste data file.
    """
    return rgba_to_image(*data_to_rgba(data))
