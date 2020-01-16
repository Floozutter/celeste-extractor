from PIL import Image, ImageFile
import string

class Texture2DFile(ImageFile.ImageFile):
    format = "T2D"
    format_description = "Celeste's MonoGame Texture2D format"

    def _open(self):
        # set size
        dimension_bytes = self.fp.read(8)
        self._size = (
            int.from_bytes(dimension_bytes[:4], "little"),
            int.from_bytes(dimension_bytes[4:], "little")
        )

        # set mode
        trans = bool(self.fp.read(1))  # transparency boolean
        if trans:
            self.mode = "RGBA"
        else:
            self.mode = "RGB"

        # set tile (what is this)
        self.tile = [
            ("raw", (0, 0) + self.size, 9, (self.mode, 0, 1))
        ]

Image.register_open(Texture2DFile.format, Texture2DFile)
Image.register_extension(Texture2DFile.format, ".data")
