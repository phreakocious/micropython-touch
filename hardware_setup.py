TFT_MISO_PIN = 12
TFT_MOSI_PIN = 13
TFT_SCK_PIN = 14
TFT_CS_PIN = 15
TFT_DC_PIN = 21
TFT_RST_PIN = 46
TFT_BL_PIN = 47

TOUCH_MISO_PIN = 7
TOUCH_MOSI_PIN = 6
TOUCH_SCK_PIN = 4
TOUCH_CS_PIN = 5
TOUCH_IRQ_PIN = 8


from machine import Pin, SPI, SoftSPI
import gc
from drivers.ili94xx.ili9486 import ILI9486 as SSD


# Screen configuration
# (Create and export an SSD instance)
prst = Pin(TFT_RST_PIN, Pin.OUT, value=1)
pdc = Pin(TFT_DC_PIN, Pin.OUT, value=0)
pcs = Pin(TFT_CS_PIN, Pin.OUT, value=1)

# Use hardSPI (bus 1)
spi = SPI(1, 33_000_000, sck=Pin(TFT_SCK_PIN), mosi=Pin(TFT_MOSI_PIN), miso=Pin(TFT_MISO_PIN))
# Precaution before instantiating framebuf
gc.collect()
ssd = SSD(spi, height=320, width=480, dc=pdc, cs=pcs, rst=prst, usd=False)
# ssd.COLOR_INVERT = 0xFFFF
from gui.core.tgui import Display, quiet

# quiet()  # Comment this out for periodic free RAM messages
from touch.xpt2046 import XPT2046

# Touch configuration
sspi = SoftSPI(
    mosi=Pin(TOUCH_MOSI_PIN), miso=Pin(TOUCH_MISO_PIN), sck=Pin(TOUCH_SCK_PIN)
)  # 2.5MHz max

tpad = XPT2046(sspi, Pin(TOUCH_IRQ_PIN), ssd)
# To create a tpad.init line for your displays please read SETUP.md
tpad.init(320, 480, 204, 156, 3825, 3900, True, False, True)


# instantiate a Display
display = Display(ssd, tpad)
