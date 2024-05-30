# ILI9488 nano-gui driver for ili9488 18-bit displays

from .ili9486 import ILI9486


@micropython.viper
def rgb565_to_rgb666(self, source: ptr16, dest: ptr8, length: int):
    for i in range(length):
        # Extracting 16-bit RGB565 values
        rgb565: uint = source[i]

        # Extracting RGB components
        r5 = rgb565 & 0x1F
        g6 = (rgb565 & (0x3F << 5)) >> 5
        b5 = (rgb565 & (0x1F << 11)) >> 11

        # # Convert to RGB666
        # r6 = (r5 & 0x1F) << 3
        # g6 = (g6 & 0x3F) << 2
        # b6 = (b5 & 0x1F) << 3

        r8 = (r5 * 527 + 23) >> 6
        g8 = (g6 * 259 + 33) >> 6
        b8 = (b5 * 527 + 23) >> 6

        # Writing RGB666 to destination
        dest[i * 3] = r8
        dest[i * 3 + 1] = b8
        dest[i * 3 + 2] = g8


class ILI9488(ILI9486):
    PIXFMT = b"\x66"  # 18-bit RGB666
    POST_PROCESS = rgb565_to_rgb666

    def __init__(
        self,
        spi,
        cs,
        dc,
        rst,
        height=320,
        width=480,
        usd=False,
        mirror=False,
        init_spi=False,
    ):
        super().__init__(spi, cs, dc, rst, height, width, usd, mirror, init_spi)
        self._outbuf = bytearray(self._short * 3)
