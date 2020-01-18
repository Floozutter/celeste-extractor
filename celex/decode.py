from typing import Tuple, List
from io import RawIOBase
from PIL import Image

Size= Tuple[int, int]  # width, height


def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, "little")


def data_to_raw(encoded: bytes) -> (bytes, Size):
    # read size
    width  = bytes_to_int(encoded[0:4])
    height = bytes_to_int(encoded[4:8])

    # check if transparency is enabled
    trans = bool(encoded[8])
    
    # preapre to convert run-length encoding to raw
    rawbytes = bytearray()
    iterbytes = iter(encoded[9:])
    
    reps = next(iterbytes, None)
    while reps is not None:
        # get opacity byte
        if trans:
            o = next(iterbytes)
        else:
            o = 255

        # get color bytes
        if o == 0:
            b = 0  # color bytes aren't encoded
            g = 0  # when opacity is zero
            r = 0
        else:
            b = next(iterbytes)
            g = next(iterbytes)
            r = next(iterbytes)

        # write to bytearray
        for i in range(reps):
            rawbytes.extend(bytes( (r, g, b, o) ))
            
        reps = next(iterbytes, None)
        
    return bytes(rawbytes), (width, height)


def raw_to_image(rawbytes: bytes, size: Size) -> Image:
    return Image.frombytes("RGBA", size, rawbytes)


def decode(texture2d: bytes) -> Image:
    return raw_to_image(*data_to_raw(texture2d))
